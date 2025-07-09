import subprocess
import json

def call_validUrl_js(url):
    """
    Appelle validUrl.js avec Node et lui passe 'url' en paramètre.
    Retourne le JSON parsé ou None en cas de problème.
    """
    # Lance la commande node /app/services/validUrl.js <url>
    try:
        process = subprocess.run(
            ["node", "/app/app/services/validUrl.js", url],
            capture_output=True,
            text=True
        )
        # Si le script Node s'est mal terminé
        if process.returncode != 0:
            print("Erreur lors de l'appel à Node :")
            print(process.stderr)  # Affiche l'erreur renvoyée par Node
            return None

        # Tente de parser la sortie comme JSON
        try:
            output_json = json.loads(process.stdout)
            return output_json
        except json.JSONDecodeError as e:
            print("Impossible de parser la sortie JSON :", e)
            print("Sortie brute Node :", process.stdout)
            return None
    except Exception as e:
        print(f"Erreur dans call_validUrl_js : {str(e)}")
        return None