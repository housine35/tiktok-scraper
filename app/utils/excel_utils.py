# app/utils/excel_utils.py
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime

def save_to_excel(
    posts: Optional[List[Dict]] = None,
    followers: Optional[List[Dict]] = None,
    following: Optional[List[Dict]] = None,
    user_info: Optional[Dict] = None,
    comments: Optional[List[Dict]] = None,
    file_name: str = "output.xlsx"
) -> None:
    """
    Sauvegarde les données TikTok dans un fichier Excel avec plusieurs onglets.
    
    Args:
        posts: Liste des publications TikTok.
        followers: Liste des followers.
        following: Liste des utilisateurs suivis.
        user_info: Informations sur l'utilisateur.
        comments: Liste des commentaires.
        file_name: Nom du fichier Excel à générer.
    """
    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        # Onglet pour les informations utilisateur
        if user_info:
            user_df = pd.DataFrame([user_info])
            user_df.to_excel(writer, sheet_name="User_Info", index=False)

        # Onglet pour les publications
        if posts:
            posts_df = pd.DataFrame(posts)
            posts_df.to_excel(writer, sheet_name="Posts", index=False)

        # Onglet pour les followers
        if followers:
            followers_df = pd.DataFrame(followers)
            followers_df.to_excel(writer, sheet_name="Followers", index=False)

        # Onglet pour les utilisateurs suivis
        if following:
            following_df = pd.DataFrame(following)
            following_df.to_excel(writer, sheet_name="Following", index=False)

        # Onglet pour les commentaires
        if comments:
            comments_df = pd.DataFrame(comments)
            comments_df.to_excel(writer, sheet_name="Comments", index=False)

    print(f"✅ Fichier Excel '{file_name}' généré avec succès.")