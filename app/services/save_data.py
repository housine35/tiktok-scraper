import pandas as pd
from openpyxl import Workbook


def clean_dataframe(df):
    """
    Nettoie un DataFrame en supprimant les caractères spéciaux
    et en s'assurant qu'il est bien formaté pour Excel.
    """
    return df.astype(str).replace({r"[\x00-\x1F\x7F]": ""}, regex=True)


def save_data_to_excel(posts, followers, following, user_info, comments, file_name):
    """
    Sauvegarde toutes les données collectées dans un fichier Excel avec plusieurs feuilles.
    """
    # Vérifier et créer les DataFrames
    posts_df = pd.DataFrame(posts) if posts else pd.DataFrame()
    followers_df = pd.DataFrame(followers) if followers else pd.DataFrame()
    following_df = pd.DataFrame(following) if following else pd.DataFrame()
    comments_df = pd.DataFrame(comments) if comments else pd.DataFrame()

    # Nettoyage des DataFrames
    if not posts_df.empty:
        posts_df = clean_dataframe(posts_df)
    if not followers_df.empty:
        followers_df = clean_dataframe(followers_df)
    if not following_df.empty:
        following_df = clean_dataframe(following_df)
    if not comments_df.empty:
        comments_df = clean_dataframe(comments_df)

    # Créer un DataFrame avec les informations utilisateur
    user_info_df = pd.DataFrame([user_info])

    try:
        # Écriture des données dans le fichier Excel
        with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
            user_info_df.to_excel(writer, sheet_name="User Info", index=False)
            if not posts_df.empty:
                posts_df.to_excel(writer, sheet_name="Posts", index=False)
            if not followers_df.empty:
                followers_df.to_excel(writer, sheet_name="Followers", index=False)
            if not following_df.empty:
                following_df.to_excel(writer, sheet_name="Following", index=False)
            if not comments_df.empty:
                comments_df.to_excel(
                    writer, sheet_name="Comments & Replies", index=False
                )  # Nouvelle feuille

        print(f"\n📁 Données sauvegardées avec succès dans {file_name}")
    except Exception as e:
        print(f"\n❌ Erreur lors de la sauvegarde du fichier : {e}")
