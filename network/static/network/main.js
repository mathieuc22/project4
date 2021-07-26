document.addEventListener('DOMContentLoaded', function() {

    // Récupération du nom de la page pour déclencher les bonnes fonctions
    const path = window.location.pathname;
    const page = path.split("/").pop();
  
    // Sélection des fonctions à exécuter en fonction de la page courante
    switch (page) {
      case "":
      case "index.html":
        // Clear out composition fields
        document.querySelector('#compose-body').value = '';
        // Prevent submit on form and call the compose API
        document.querySelector('#compose-form').addEventListener('submit', send_post);
        break;
    }
  
    // Like Unlike logic on hearts
    document.querySelectorAll('.button-like').forEach(button => { button.addEventListener('click', (event) => like_post(event)) });
  
  });
  
  function send_post(event) {
    
    // prevent the refresh due to form submission
    event.preventDefault();
  
    // Use the API to send the mail
    fetch('/posts/new', {
      method: 'POST',
      body: JSON.stringify({
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
  
    // set wait to let the request return
    setTimeout(() => {document.location.reload();}, 100);
  }
  
  function like_post(event) {
  
    // prevent the refresh due to form submission
    event.preventDefault();
    const id = event.target.id.split('-')[1]
    const likeButton = document.querySelector(`#like-${id}`)
    let likeTag
  
    if (likeButton.classList[0]==='far') {
      likeTag = 1
      likeButton.setAttribute('class','fas fa-heart');
    } else {
      likeTag = 0
      likeButton.setAttribute('class','far fa-heart');
    }
  
    fetch(`/posts/${id}`, {
      method: 'PUT',
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
          like: likeTag
      })
    })
    .then(response => response.json())
    .then(post => {
        // Print result
        console.log(post);
        document.querySelector(`#nblikes-${id}`).innerHTML = post.nbLikes
    });
  
  
  }
  