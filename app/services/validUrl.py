import subprocess
import json
import os


def call_validUrl_js(url):
    """
    Appelle validUrl.js avec Node et lui passe 'url' en paramètre.
    Retourne le JSON parsé ou None en cas de problème.
    """
    script_path = "/app/services/validUrl.js"
    print(f"Tentative d'exécution de Node avec le script : {script_path}")
    if not os.path.exists(script_path):
        print(f"Erreur : Le fichier {script_path} n'existe pas dans le conteneur")
        return None

    try:
        process = subprocess.run(
            ["node", script_path, url], capture_output=True, text=True
        )
        if process.returncode != 0:
            print("Erreur lors de l'appel à Node :")
            print(process.stderr)
            return None

        try:
            output_json = json.loads(process.stdout)
            print(f"Résultat de validUrl.js : {output_json}")
            return output_json
        except json.JSONDecodeError as e:
            print("Impossible de parser la sortie JSON :", e)
            print("Sortie brute Node :", process.stdout)
            return None
    except Exception as e:
        print(f"Erreur dans call_validUrl_js : {str(e)}")
        return None
