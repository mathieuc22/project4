
document.addEventListener("DOMContentLoaded", function () {
  
    document.querySelectorAll(".like-button").forEach(likeButton => {
        const params = likeButton.name.split('--')
        console.log(params);
        likeButton.addEventListener("click", () => likeUnlike(params));
    })

});

function likeUnlike(params) {
    console.log(params);
    fetch('/like', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({'post':params[0], 'user':params[1]}) //JavaScript object of data to POST
    })
    .then(response => {
        return response.json() //Convert response to JSON
    })
    .then(data => {
        //Perform actions with the response data from the view
        console.log(data)
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}