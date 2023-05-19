def test_like(authorized_client, post_create):
    response = authorized_client.post("/vote/", json={"post_id": 1, "like": 1})
    assert response.status_code == 201
    
    
def test_already_liked(authorized_client, like_create):
    response = authorized_client.post("/vote/", json={"post_id": 1, "like": 1})
    assert response.status_code == 400
    assert response.json()['detail'] == "You already voted this post"
    
    
def test_dislike(authorized_client, post_create):
    response = authorized_client.post("/vote/", json={"post_id": 1, "like": 1})
    assert response.status_code == 201
    response = authorized_client.post("/vote/", json={"post_id": 1, "like": 0})
    assert response.status_code == 201
    
 
def test_already_disliked(authorized_client, post_create):
    response = authorized_client.post("/vote/", json={"post_id": 1, "like": 0})
    assert response.status_code == 400
    assert response.json()['detail'] == "You didn't vote this post"