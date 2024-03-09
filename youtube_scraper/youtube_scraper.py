from youtubesearchpython import VideosSearch

def scrape_youtube_data(query, max_results=5):
    videos_search = VideosSearch(query, limit=max_results)
    results = videos_search.result()

    video_data_list = []

    for video in results['result']:
        video_data = {
            'url': video['link'],
            'thumbnail': video['thumbnails'][0]['url'],
            'title': video['title'],
            # 'description': video['description']
        }
        video_data_list.append(video_data)

    return video_data_list

search_query = "python programming tutorial"
max_results = 5
video_data_list = scrape_youtube_data(search_query, max_results)

for index, video_data in enumerate(video_data_list, start=1):
    print(f"Video {index} - Title: {video_data['title']}")
    print(f"  URL: {video_data['url']}")
    print(f"  Thumbnail: {video_data['thumbnail']}")
    # print(f"  Description: {video_data['description']}")
    print("\n")
