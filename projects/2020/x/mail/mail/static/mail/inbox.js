document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

})


function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
  // Add submit function
  form = document.querySelector('#compose-form');
  form.onsubmit = function() {
    const recipient = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body =  document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipient,
        subject: subject,
        body: body
      })
    })
    .then(response => {
      if (response.status === 201) {
        load_mailbox('sent');
      } else {
        response.json().then(data => {
          alert(data['error'])
        })
      }
    })
    
    // Prevents default submit action
    return false;
  }
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  create_table(mailbox);
}


function create_table(mailbox) {

  fetch(`/emails/${mailbox}`)
  .then(response => {
    response.json().then(data => {
      // Creation of Table + Headers
      const email_view = document.querySelector('#emails-view');
      const table = document.createElement('table');
      const who = (mailbox === 'sent') ? 'To' : 'From';
      table.className = 'table table-hover table-sm';

      table.innerHTML = `
                        <thead class="thead-dark">
                          <tr>
                            <th style="width: 25%" scope="col">${who}</th>
                            <th style="width: 55%" scope="col">Subject</th>
                            <th style="width: 20%" scope="col">Date</th>
                          </tr>
                        </thead>`;

      email_view.append(table);
      // End of Table Creation

      for (let i=0; i < data.length; i++) {
        const new_row = document.createElement('tbody');
        const address = (mailbox === 'sent') ? data[i].recipients : data[i].sender;
        const subject = (data[i].subject.length > 70) ? data[i].subject.slice(0, 67) + ' ...' : data[i].subject;
        const time = data[i].timestamp;
        const id = data[i].id;

        // Read background to grey as per specifications
        if (data[i].read === true) {
          new_row.className = 'table-active';
        }

        new_row.innerHTML = `<tr>
                              <th scope="col">${address}</th>
                              <th scope="col">${subject}</th>
                              <th scope="col">${time}</th>
                            </tr>`;

        new_row.addEventListener('click', function() {
          fetch(`/emails/${id}`)
          .then(response => response.json().then(email => show_email(email, mailbox)))
        })

        // Insert email into table  
        table.insertBefore(new_row,null);
      }
    })
  })
}


function show_email(email, mailbox) {
  const subject = email.subject;
  const recipient = email.recipients.join('; ');
  const sender = email.sender;
  const body = email.body;
  const date = email.timestamp;
  const table = document.createElement('table');
  table.className = 'table table-sm';

  table.innerHTML = `
                    <thead class="">
                      <tr>
                        <th style="width: 15%" scope="row">Recipient</th>
                        <td style="width: 85%">${recipient}</td>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <th scope="row">Sender</th>
                        <td>${sender}</td>
                      </tr>
                    </tbody>
                    <tbody>
                      <tr>
                        <td colspan="2"><pre>${body}</pre></td>
                      </tr>
                    </tbody>
                    `;

    document.querySelector('#emails-view').innerHTML = `<h2>${subject}<small class="float-right">${date}</small></h2>`;
    document.querySelector('#emails-view').append(table);
    const buttons = document.createElement('div');
    buttons.className = 'mt-2';
    const reply = document.createElement('button');
    reply.className = 'btn btn-primary';
    reply.innerHTML = 'Reply';
    reply.addEventListener('click', function() {
          compose_email();
          document.querySelector('#compose-recipients').value = sender;
          document.querySelector('#compose-subject').value = (subject.slice(0,4) === 'Re: ') ? subject : 'Re: ' + subject;
          document.querySelector('#compose-body').value = `On ${date} ${sender} wrote: ${body}`;
    })

    buttons.append(reply);

    if (mailbox != 'sent') {
      const archive = document.createElement('button');
      if (email.archived === false) {
        archive.innerHTML = 'Archive';;
        archive.className = 'btn btn-danger float-right';
        archive.addEventListener('click', function() {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: true
            })
          }).then(() => load_mailbox('inbox'));
        })
      } else {
        archive.innerHTML = 'Unarchive';;
        archive.className = 'btn btn-warning float-right';
        archive.addEventListener('click', function() {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: false
            })
          }).then(() => load_mailbox('inbox'));
        })
      }
      buttons.append(archive)
    }

  document.querySelector('#emails-view').append(buttons);

  if (email.read === false) {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
  }
}