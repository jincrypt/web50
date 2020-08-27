document.addEventListener('DOMContentLoaded', function() {
  // By default, load the inbox
  follow_unfollow()
})

function follow_unfollow() {
  followers();
  if (document.querySelector('#buttons')) {

    // how do i know if the user is following this profile?
    const button_div = document.querySelector('#buttons')
    const owner = button_div.dataset["name"]
    fetch(`/UserRelationship/${owner}`)
    .then(response => {
      // If User is Currently Following, then present an Unfollow button
      if (response.status === 204) {
        const unfollow_button = document.createElement('button')
        unfollow_button.setAttribute('id', 'unfollow_button')
        unfollow_button.className = 'btn btn-secondary'
        unfollow_button.innerHTML = 'Unfollow'
        unfollow_button.addEventListener('click', () => {
          unfollow_button.disabled = true;
          fetch(`/UserRelationship/${owner}`, {
            credentials: 'include',
            method: 'PUT',
            headers: {'X-CSRFToken': getCookie('csrftoken')}
          })
          .then(response => {
            if (response.status === 204) {
              follow_unfollow()
            } else {
              response.json().then(data => {
                alert(data["message"])
              })
            }
          })
        })
        button_div.innerHTML= ''
        button_div.appendChild(unfollow_button)
        console.log('204')
      } else {
        console.log(response.status)
        const follow_button = document.createElement('button')
        follow_button.setAttribute('id', 'follow_button')
        follow_button.className = 'btn btn-primary'
        follow_button.innerHTML = 'Follow'
        follow_button.addEventListener('click', () => {
          follow_button.disabled = true;
          fetch(`/UserRelationship/${owner}`, {
            credentials: 'include',
            method: 'PUT',
            headers: {'X-CSRFToken': getCookie('csrftoken')}
          })
          .then(response => {
            if (response.status === 204) {
              follow_unfollow()
            } else {
              response.json().then(data => {
                alert(data["message"])
              })
            }
          })
        })
        button_div.innerHTML= ''
        button_div.appendChild(follow_button)
      }
    })
  }
}

function followers() {
  const counter = document.querySelector('#followers');
  const owner = document.querySelector('#owner').dataset['name'];
  fetch(`/followers/${owner}`)
  .then(response => {
    response.json().then(data => {
      counter.innerHTML = data['follower_count']
    })
  })
}

// From https://docs.djangoproject.com/en/3.1/ref/csrf/
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