import yt_dlp
import csv

# Définition des mots-clés pour la recherche
keywords = ['Mohammed VI', 'Mohammed 6', 'King of Morocco', 'Roi du Maroc', 'محمد السادس']

# Plateformes à scraper
platforms = {
    "YouTube": "ytsearch10:",  # Recherche les 10 premiers résultats sur YouTube
    "Dailymotion": "dmsearch10:"  # Recherche les 10 premiers résultats sur Dailymotion
}

# Liste pour stocker les résultats
audio_data = []

# Fonction pour extraire les liens MP3
def scrape_audio_links(platform, search_query):
    ydl_opts = {
        'quiet': True,  # Désactiver les logs inutiles
        'extract_flat': True,  # Ne pas télécharger, seulement extraire les métadonnées
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_url = platforms[platform] + search_query
        try:
            info = ydl.extract_info(search_url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    if entry:  # Vérifier que l'entrée est valide
                        # Récupérer le lien audio MP3
                        audio_url = extract_audio_link(entry['url'])
                        if audio_url:
                            audio_data.append([platform, search_query, entry['title'], audio_url])
        except Exception as e:
            print(f" Erreur lors du scraping sur {platform} avec '{search_query}': {e}")

# Fonction pour obtenir le lien direct du fichier audio
def extract_audio_link(video_url):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',  # Extraire seulement l’audio
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convertir en MP3
            'preferredquality': '192',  # Qualité audio
        }],
        'noplaylist': True,
        'simulate': True,  # Ne pas télécharger, juste extraire les liens
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            if 'url' in info:
                return info['url']  # Retourne le lien direct du fichier audio MP3
        except Exception as e:
            print(f" Erreur lors de l'extraction de l'audio pour {video_url}: {e}")
    return None

# Exécuter le scraping pour chaque mot-clé et chaque plateforme
for keyword in keywords:
    for platform in platforms.keys():
        scrape_audio_links(platform, keyword)

# Enregistrer les résultats dans un fichier CSV
csv_filename = "audio_links.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Plateforme", "Mot-clé", "Titre", "Lien Audio MP3"])  # En-têtes
    writer.writerows(audio_data)

print(f" Scraping terminé ! Les liens MP3 sont enregistrés dans {csv_filename}.")
