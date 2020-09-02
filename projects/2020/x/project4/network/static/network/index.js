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
{/* <div id="post">
  <div id="user">
    <a href="/profile/frasulov">frasulov</a>
  </div>
  <div class="detail">
    <h3>Fagan</h3>
    <div>Iyiyim sen nasilsin?</div>
    <div class="text-muted" style="font-size: 14px;">
      August 03, 2020 09:31:23
    </div>
    <div>
      <span>
        <i style="color:red" class="fas fa-heart" aria-hidden="true"></i>
        3 people liked
      </span>
    </div>
  </div>
</div> */} 




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
        const likes = data[i]['likes']

        new_post.className = 'mb-2'
        new_post.style = 'border-bottom: 1px dotted #ccc'

        new_post.innerHTML = `
                              <div class="media container mt-2">
                                  <div class="media-body">
                                      <h5 class="media-heading user_name" style="font-size:14px; font-weight: bold">
                                      <a href='profile/${owner}'>${ owner }</a>
                                      </h5>
                                      <p class="float-right"><small>${ timestamp }</small></p></h5>
                                      <p data-id=${ post_id }>${ body }</p>
                                      <p data-likesid=${ post_id }>${ likes }</p>
                                  </div>
                              </div>`

        if (owner == document.querySelector("#current_user").innerText) {
          const edit = document.createElement('button');
          edit.innerHTML="Edit";
          edit.className = 'btn btn-primary';
          edit.setAttribute('data-id', post_id);
          edit.addEventListener('click', () => edit_post(post_id))
          new_post.appendChild(edit)
        } else {
          const likebutton = document.createElement('button');

          // like_unlike returns a promise object. So we need to callback to apply the result
          like_unlike(post_id)
          .then(result => {
            likebutton.innerHTML= result
          });
          likebutton.className = 'btn btn-primary';
          likebutton.setAttribute('data-likesid', post_id);
          // likebutton.addEventListener('click', () => edit_post(post_id))
          new_post.appendChild(likebutton)
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

async function like_unlike(post_id) {
  let response = await fetch(`/like/${post_id}`)
  let result = response.status;
  console.log(result)
  let test = ''
  if (result === 204) {
    test = 'Unlike'
  } else {
    test ='Like'
  }
  console.log(result, test)
  return test
}
//  !! Doesnt work. Promises have to resolve before it returns.... back to the drawing board for likes
// function like_unlike(post_id) {
//   const button_div = document.createElement('div')
//   var result = ''
//   fetch(`/like/${post_id}`)
//   .then(response => {
//     if (response.status === 204) {
//       // const like_button = document.createElement('button')
//       // like_button.className = 'btn btn-secondary'
//       // like_button.innerHTML = 'Like'
//       result = 'Hello';

//     } else {
//       // const unlike_button = document.createElement('button')
//       // unlike_button.className = 'btn btn-secondary'
//       // unlike_button.innerHTML = 'Unlike'

//       // button_div.innerHTML= ''
//       // button_div.appendChild(unlike_button)
//       console.log('test')
//       result = 'bye'

//     }
//   })
//   .then(response=>{
//     return result})
// }
