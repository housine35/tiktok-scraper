from fastapi import APIRouter, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
import re
import os
from datetime import datetime
from app.services.get_secuid import get_secuid
from app.services.get_posts import fetch_all_posts
from app.services.get_comments import fetch_comments
from app.services.get_followers import fetch_followers
from app.services.get_following import fetch_following
from app.utils.excel_utils import save_to_excel

router = APIRouter()

@router.post("/scrape_tiktok_data/")
async def scrape_tiktok_data(
    background_tasks: BackgroundTasks,
    tiktok_account: str = Form(...),
    data_type: list[str] = Form([])
):
    try:
        # Étape 1 : Extraire le nom d'utilisateur de l'URL TikTok
        match = re.search(r"@([a-zA-Z0-9_.-]+)", tiktok_account)
        username = match.group(1) if match else "default_user"
        print(f"Nom d'utilisateur extrait ou par défaut : {username}")

        # Étape 2 : Récupérer le secUid
        secuid = get_secuid(tiktok_account)
        print(f"secUid récupéré : {secuid}")
        if "Error" in secuid or "not found" in secuid:
            return JSONResponse(
                content={"error": f"Erreur lors de la récupération du secUid : {secuid}"},
                status_code=400
            )

        # Étape 3 : Initialiser les données collectées
        posts, followers, following_data, user_info, all_comments = None, None, None, None, None

        if "comments" in data_type and "posts" in data_type:
            print("📥 Récupération des publications et des commentaires...")
            posts_data = fetch_all_posts(secuid)
            if posts_data and posts_data.get("posts"):
                user_info = posts_data.get("user", {})
                posts = posts_data["posts"]

                all_comments = []
                for post in posts:
                    if post.get("commentCount"):
                        comments = fetch_comments(post["id"])
                        all_comments.extend(comments)

                print(f"✅ Total des commentaires récupérés : {len(all_comments)}")

        elif "posts" in data_type:
            print("📥 Récupération des publications...")
            posts_data = fetch_all_posts(secuid)
            if posts_data and posts_data.get("posts"):
                user_info = posts_data.get("user", {})
                posts = posts_data["posts"]

        if "followers" in data_type:
            print("📥 Récupération des followers...")
            followers = fetch_followers(secuid)

        if "following" in data_type:
            print("📥 Récupération des utilisateurs suivis...")
            following_data = fetch_following(secuid)

        # Étape 5 : Générer le nom du fichier basé sur l'utilisateur
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{username}_{timestamp}.xlsx"

        # Étape 6 : Sauvegarder les données dans un fichier Excel
        save_to_excel(posts, followers, following_data, user_info, all_comments, file_name)

        # Étape 7 : Supprimer le fichier temporaire après le téléchargement
        background_tasks.add_task(os.remove, file_name)

        # Retourner le fichier en réponse
        return FileResponse(
            path=file_name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=file_name,
        )

    except Exception as e:
        print(f"Erreur capturée : {str(e)}")  # Débogage
        return JSONResponse(content={"error": f"Erreur lors du traitement des données : {str(e)}"}, status_code=500)