document.addEventListener('DOMContentLoaded', function() {

    // Récupération du nom de la page pour déclencher les bonnes fonctions
    const path = window.location.pathname;
    const page = path.split("/").pop();
  
    console.log(page);
    // Sélection des fonctions à exécuter en fonction de la page courante
    switch (page) {
      case "":
      case "posts":
          // Like Unlike logic on hearts
          document.querySelectorAll('.button--like').forEach(button => { button.addEventListener('click', (event) => like_post(event)) });
          // Edit users posts
          document.querySelectorAll('.button--edit').forEach(button => { button.addEventListener('click', edit_post) });

        break;
      case "following":
        document.getElementById('compose-view').style.display = 'none';
        document.querySelector('h1').innerHTML = 'Following'
    }
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
  
  function edit_post(event) {
    
    // remove the existing event on the button
    const button = event.target;
    button.removeEventListener('click', edit_post);
    button.classList.add('button--save')
    button.innerHTML = 'Save';
    button.addEventListener('click', save_post);

    // create the textarea and hide the paragraph
    const id = button.id.split('-')[2];
    console.log(id)
    const postContainter = document.querySelector(`#post-container-${id}`);
    const postText = document.querySelector(`#post-content-${id}`);
    postText.style.display = 'none'
    const postEdit = document.createElement("textarea");
    postEdit.setAttribute('class','form-control posts__textarea');
    postEdit.setAttribute('rows','3');
    postEdit.setAttribute('id',`post-edit-${id}`);
    postEdit.innerHTML = postText.innerHTML.replace(/<br\s*[\/]?>/gi, "\n");
    postContainter.appendChild(postEdit);


    // <textarea class="form-control" id="compose-body" placeholder="Body"></textarea>

  }

  function save_post(event) {

    // remove the existing event on the button
    const button = event.target;
    const id = button.id.split('-')[2];
    const postText = document.querySelector(`#post-content-${id}`);
    const postEdit = document.querySelector(`#post-edit-${id}`);

    if (postEdit.value) {
      fetch(`/posts/${id}`, {
        method: 'PUT',
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: postEdit.value
        })
      })
      .then(response => response.json())
      .then(post => {
          // Print result
          postText.removeAttribute('style');
          postText.innerHTML = post.newText.replace(/\n/g, '<br />');
          postEdit.remove();
          button.innerHTML = 'Edit';
          button.classList.remove('button--primary')
          button.addEventListener('click', edit_post);
      });
    }
  }
  
  function like_post(event) {
  
    // prevent the refresh due to form submission
    event.preventDefault();
    const id = event.target.id.split('-')[1]
    const likeButton = document.querySelector(`#like-${id}`)
    let likeTag
  
    if (likeButton.classList[0]==='far') {
      likeTag = 1
      likeButton.setAttribute('class','fas fa-heart like--active');
    } else {
      likeTag = 0
      likeButton.setAttribute('class','far fa-heart like');
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
  