def test_config(api_client):
    response = api_client.get("/info")
    result = response.json()
    print(result)


def test_tracks_api(api_client, track_db):
    response = api_client.get("/api/tracks")
    assert response.status_code == 200

    track_json = response.json()[0]
    assert track_json["artist"] == track_db.artist
    assert track_json["title"] == track_db.title
