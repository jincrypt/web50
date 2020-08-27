document.addEventListener('DOMContentLoaded', function() {
  // By default, load the inbox
  all_posts();
  new_post();
})

function load_post(post_id) {
  fetch(`posts/${ post_id }`)
  .then(response => response.json())
  .then(post => {
    console.log(post)
    const area = document.querySelector(`p[data-id="${ post_id }"]`)
    const edit_button = document.querySelector(`button[data-id="${ post_id }"]`)
    area.innerHTML = post.body;
    edit_button.removeAttribute('style')
  })
}


function all_posts() {
    const all_posts = document.querySelector('#all_posts');
    all_posts.innerHTML = ''
    fetch('/posts')
    .then(response => response.json())
    .then(data => {
      for (let i=0; i < data.length; i++) {
        const body = data[i].body;
        const owner = data[i].user;
        const timestamp = data[i].timestamp;
        const new_post = document.createElement('div')
        const post_id = data[i]['id']

        new_post.className = 'mb-2'
        new_post.style = 'border-bottom: 1px dotted #ccc'

        new_post.innerHTML = `
                              <div class="media container mt-2">
                                  <div class="media-body">
                                      <h5 class="media-heading user_name" style="font-size:14px; font-weight: bold">${ owner }
                                      <p class="float-right"><small>${ timestamp }</small></p></h5>
                                      <p data-id=${ post_id }>${ body }</p>
                                  </div>
                              </div>`

        if (owner == document.querySelector("#current_user").innerText) {
          const edit = document.createElement('button');
          edit.innerHTML="Edit";
          edit.className = 'btn btn-primary';
          edit.setAttribute('data-id', post_id);
          edit.addEventListener('click', () => edit_post(post_id))
          new_post.appendChild(edit)
        }

        all_posts.append(new_post);
      }
      console.log(data);
    })
}


function edit_post(post_id) {
  // Hide Edit Button
  const edit_button = document.querySelector(`button[data-id="${post_id}"]`)
  edit_button.setAttribute('style', 'display:none')

  const current_body = document.querySelector(`p[data-id="${post_id}"]`);
  const original_text = current_body.innerHTML;
  const text_area = document.createElement('textarea');

  const submit = document.createElement('button');
  submit.className = "btn btn-primary"
  submit.innerHTML = "Submit"

  submit.addEventListener('click', () => {
    console.log(post_id)
    fetch(`/edit_post/${ post_id }`, {
      credentials: 'include',
      method: 'PUT',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: JSON.stringify({
          new_body: `${text_area.value}`
      })
    })
    .then(response => {
      if (response.status === 204) {
        load_post(post_id);
      } else {
        response.json().then(data => {
          alert(data["message"])
        })
      }
    })
  })
  
  const cancel = document.createElement('button');
  cancel.className = "btn btn-primary"
  cancel.innerHTML = "Cancel"

  cancel.addEventListener('click', () => {
    current_body.innerHTML = original_text;
    edit_button.removeAttribute('style');
  })

  const button_div = document.createElement('div');
  button_div.append(cancel);
  button_div.append(submit);

  text_area.value = current_body.innerHTML;
  current_body.innerHTML = ''
  current_body.append(text_area)
  current_body.appendChild(button_div)

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

function new_post() {
    // Clear out composition fields
    document.querySelector('#new_post-body').value = '';

    // Add submit function
    form = document.querySelector('#new_post-form');
    form.onsubmit = function() {
        const body =  document.querySelector('#new_post-body').value;

    fetch('/posts', {
        credentials: 'include',
        method: 'POST',
        mode: 'same-origin',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        body: JSON.stringify({
                body: body,
            })
        })
    .then(response => {
      if (response.status === 201) {
        all_posts();
      } else {
        response.json().then(data => {
          alert(data["message"])
        })
      }
    })
    
    // CLears
    document.querySelector('#new_post-body').value = ''
    // Prevents default submit action
    return false;
  }
}