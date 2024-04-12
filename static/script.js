function change_values(){  // for account-profile.html
    let form = new FormData()

    let surname = document.getElementById('surname').innerHTML
    let name = document.getElementById('name').innerHTML
    let username = document.getElementById('username').innerHTML
    let email = document.getElementById('email').innerHTML

    form.append('surname', surname)
    form.append('name', name)
    form.append('username', username)
    form.append('email', email)



    fetch(window.location.href, {
        method: 'POST',
        body: form
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if(data.errors){
            throw_errors(data)
        }
        else{
            window.location.replace('/account/@' + data.current_values['username'])
        }
    })

}



function throw_errors(data){  // for account-profile.html
    let errors = data.errors
    let values = data.current_values
    
    for (const key in errors) {
        if (Object.hasOwnProperty.call(errors, key)) {
          const errorMessages = errors[key];
          
          for (const errorMessage of errorMessages) {
            create_toast(errorMessage)

            document.getElementById(key).innerHTML = values[key]
          }
        }
      }
}


let n = 0
let toasts_to_delete = []
function create_toast(message, type='error'){  // for account-profile.html
    toast_container = document.getElementById('toast-container')

    if (type=='error'){
        toast_container.innerHTML += `<div class="toast my-2" role="alert" aria-live="assertive" aria-atomic="true" id='toast ` + (n+1) + `'>
        <div class="alert alert-danger d-flex align-items-center m-0" role="alert">
            <div>
                <strong>Ошибка!</strong> ` + message + `
            </div>
        </div>
        </div>`
    }
    else{
        toast_container.innerHTML += `<div class="toast my-2" role="alert" aria-live="assertive" aria-atomic="true" id='toast ` + (n+1) + `'>
        <div class="alert alert-success d-flex align-items-center m-0" role="alert">
            <div>
                <strong>Успех!</strong> ` + message + `
            </div>
        </div>
        </div>`
    }

    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl);
    });
    toastList.forEach(function (toast) {
        toast.show();
    });
    
    n++
    toasts_to_delete.push('toast ' + n)
    setTimeout(() => {
        let elem = document.getElementById(toasts_to_delete[0])
        toasts_to_delete.shift()
        elem.remove()
    }, 6000);
}


function change_password_request(){  // for account-profile.html
    let form = new FormData()

    let oldPassword = document.getElementById('oldPassword').value
    let newPassword = document.getElementById('newPassword').value

    form.append('oldPassword', oldPassword)
    form.append('newPassword', newPassword)

    fetch(window.location.href + '/password', {
        method: 'POST',
        body: form
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        if (data.errors){
            throw_errors(data, undefined)
        }
        else{
            create_toast('Пароль изменён.', 'success')
        }
    })
}



function textarea_auto_resize(){  // for create-project-form.html
    const textarea = document.getElementById('description');
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}



function change_description_vision(n){  // for account-projects.html
    var selection = window.getSelection().toString();

    if (!selection) {
        let short_description = document.getElementById('short_description ' + n)
        let all_description = document.getElementById('all_description ' + n)

        if (short_description.hidden){
            short_description.hidden = false
            all_description.hidden = true
        }
        else{
            short_description.hidden = true
            all_description.hidden = false
        }
    }
}


function delelte_project_request(project_id){  // for account-projects.html
    let form = new FormData();
    form.append('project_id', project_id)

    fetch('/project/' + project_id + '/delete', {
        method: 'POST',
        body: form
    })
    .then(respone => {
        return respone.json()
    })
    .then(data => {
        if (data.status == 'ok'){
            window.location.reload()
        }
    })

}