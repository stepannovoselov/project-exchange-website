function change_values(){  // for account-profile.html
    show_spinner()

    let form = new FormData()

    let surname = document.getElementById('surname')
    let surname_value = surname.value !== undefined ? surname.value : ""

    let name = document.getElementById('name')
    let name_value = name.value !== undefined ? name.value : ""

    let username = document.getElementById('username')
    let username_value = username.value !== undefined ? username.value : ""

    let email = document.getElementById('email')
    let email_value = email.value !== undefined ? email.value : ""

    let vk_link = document.getElementById('vk_link')
    let vk_link_value = (vk_link.value !== undefined && vk_link.value !== 'Не указано') ? vk_link.value : ""

    let telegram_link = document.getElementById('telegram_link')
    let telegram_link_value = (telegram_link.value !== undefined && telegram_link.value !== 'Не указано') ? telegram_link.value : ""

    let github_link = document.getElementById('github_link')
    let github_link_value = (github_link.value !== undefined && github_link.value !== 'Не указано') ? github_link.value : ""

    let email_link = document.getElementById('email_link')
    let email_link_value = (email_link.value !== undefined && email_link.value !== 'Не указано') ? email_link.value : ""

    let education = document.getElementById('education')
    let education_value = education.value !== undefined ? education.value : ""

    let skills = document.getElementById('skills')
    let skills_value = skills.value !== undefined ? skills.value : ""

    let hobbies = document.getElementById('hobbies')
    let hobbies_value = hobbies.value !== undefined ? hobbies.value : ""

    let tags = document.getElementById('tags')
    let tags_value = tags.value !== undefined ? tags.value : ""


    form.append('surname', surname_value)
    form.append('name', name_value)
    form.append('username', username_value)
    form.append('email', email_value)
    form.append('vk_link', vk_link_value)
    form.append('telegram_link', telegram_link_value)
    form.append('github_link', github_link_value)
    form.append('email_link', email_link_value)
    form.append('education', education_value)
    form.append('skills', skills_value)
    form.append('hobbies', hobbies_value)
    form.append('tags', tags_value)


    fetch(window.location.href, {
        method: 'POST',
        body: form
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if(data.errors){
            let errorMessages = Object.values(data.errors).flat();
            let errorMessageString = '● ' + errorMessages.join('<br>● ');
            showNotification('Ошибка при изменении данных!<br>' + errorMessageString, 'danger')
        }
        else{
            showNotification('Данные успешно изменены!<br><small>Для корректного отображения обновите страницу.</small>', 'success')
            surname = data.current_values.surname
            name = data.current_values.name
            username = data.current_values.username
            email = data.current_values.email
            vk_link = data.current_values.about.vk_link
            telegram_link = data.current_values.about.telegram_link
            github_link = data.current_values.about.github_link
            email_link = data.current_values.about.email_link
            education = data.current_values.about.education
            skills = data.current_values.about.skills
            hobbies = data.current_values.about.hobbies
            tags = data.current_values.about.tags

            document.getElementById('link-projects').setAttribute('href', '/account/@' + data.current_values.username + '/projects')
            document.getElementById('link-bookmarks').setAttribute('href', '/account/@' + data.current_values.username + '/bookmarks')
            document.getElementById('main-surname-and-name').innerHTML = data.current_values.surname + ' ' + data.current_values.name
        }
        hide_spinner()
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



function textarea_auto_resize(textarea_id){  // for create-project-form.html
    let textarea = document.getElementById(textarea_id);
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


function make_project_action(project_id, action){  // for project.html
    fetch('/project/' + project_id + '/' + action, {
        method: 'POST',
    })
    .then(respone => {
        return respone.json()
    })
    .then(data => {
        window.location.reload()
    })
}


function ai_generate_project(){  // for create-project-form.html
    show_spinner()
    
    fetch('/project/ai/generate_project', {
        method: 'GET'
    })
    .then(respone => {return respone.json()})
    .then(data => {
        if (data['Название']){
            document.getElementById('name').innerHTML = data['Название']
            textarea_auto_resize('name')
        }
        if (data['Описание']){
            document.getElementById('description').innerHTML = data['Описание']
            textarea_auto_resize('description')
        }
        if (data['Цель']){
            document.getElementById('goal').innerHTML = data['Цель']
            textarea_auto_resize('goal')
        }
        if (data['Тема']){
            document.getElementById('theme').innerHTML = data['Тема']
            textarea_auto_resize('theme')
        }
        if (data['Теги']){
            document.getElementById('tags').innerHTML = data['Теги']
            textarea_auto_resize('tags')
        }
        document.getElementById('opt1').selected = true
    
        hide_spinner()
        close_modal()
    })
}


function ai_generate_science(){  // for create-project-form.html
    show_spinner()
    
    fetch('/project/ai/generate_science', {
        method: 'GET'
    })
    .then(respone => {return respone.json()})
    .then(data => {
        if (data['Название']){
            document.getElementById('name').value = data['Название']
            textarea_auto_resize('name')
        }
        if (data['Описание']){
            document.getElementById('description').value = data['Описание']
            textarea_auto_resize('description')
        }
        if (data['Цель']){
            document.getElementById('goal').value = data['Цель']
            textarea_auto_resize('goal')
        }
        if (data['Тема']){
            document.getElementById('theme').value = data['Тема']
            textarea_auto_resize('theme')
        }
        if (data['Теги']){
            document.getElementById('tags').innerHTML = data['Теги']
            textarea_auto_resize('tags')
        }
        document.getElementById('opt2').selected = true
        
        hide_spinner()
        close_modal()
    })
}


function ai_upgrade_text(){  // for create-project-form.html
    show_spinner()
    
    let selectElement = document.getElementById("upgrade_text_selector");
    let selected_index = selectElement.selectedIndex
    
    fetch('/project/ai/upgrade_text?' + new URLSearchParams({
        'edit': ['name', 'theme', 'goal', 'description'][selected_index],
        'name': document.getElementById('name').value,
        'theme': document.getElementById('theme').value,
        'goal': document.getElementById('goal').value,
        'description': document.getElementById('description').value
    }), {
        method: 'GET'
    })
    .then(respone => {return respone.json()})
    .then(data => {
        delete data['status']
        console.log(['name', 'theme', 'goal', 'description'][selected_index])
        console.log(document.getElementById(['name', 'theme', 'goal', 'description'][selected_index]))
        console.log(document.getElementById(['name', 'theme', 'goal', 'description'][selected_index]).innerHTML)
        if (data['response']){
            data = data['response']
        }
        document.getElementById(['name', 'theme', 'goal', 'description'][selected_index]).value = Object.values(data)
        textarea_auto_resize(['name', 'theme', 'goal', 'description'][selected_index])
    
        hide_spinner()
        close_modal()
    })
}


function ai_fill_text(){  // for create-project-form.html
    show_spinner()
    
    let selectElement = document.getElementById("fill_text_selector");
    let selected_index = selectElement.selectedIndex
    
    fetch('/project/ai/fill_text?' + new URLSearchParams({
        'fill': ['name', 'theme', 'goal', 'description'][selected_index],
        'name': document.getElementById('name').value,
        'theme': document.getElementById('theme').value,
        'goal': document.getElementById('goal').value,
        'description': document.getElementById('description').value
    }), {
        method: 'GET'
    })
    .then(respone => {return respone.json()})
    .then(data => {
        delete data['status']
        console.log(['name', 'theme', 'goal', 'description'][selected_index])
        console.log(document.getElementById(['name', 'theme', 'goal', 'description'][selected_index]))
        console.log(document.getElementById(['name', 'theme', 'goal', 'description'][selected_index]).innerHTML)
        if (data['response']){
            data = data['response']
        }
        document.getElementById(['name', 'theme', 'goal', 'description'][selected_index]).value = Object.values(data)
        textarea_auto_resize(['name', 'theme', 'goal', 'description'][selected_index])
    
        hide_spinner()
        close_modal();
    })
}


function close_modal() {
    let ai_tools_modal = document.getElementById('AI_tools')

    $(ai_tools_modal).modal('hide');

}


document.getElementById('addVacancyBtn').addEventListener('click', function() {  // for create-project-form.html
    let vacancyCards = document.getElementById('vacancyCards')
    let newCard = vacancyCards.querySelector('.col-6').cloneNode(true)
    let inputs = newCard.querySelectorAll('input[type=text], textarea')
    
    newCard.classList.remove('d-none')
    
    inputs.forEach(function(input) {
      input.value = '';
    })
    
    vacancyCards.appendChild(newCard)
  });


document.addEventListener('click', function(event) {  // for create-project-form.html
if (event.target && event.target.classList.contains('delete-btn')) {
    let elem = event.target.closest('.col-6').remove()
}
});




document.getElementById('project_form').addEventListener('submit', function(event) {  // for create-project-form.html
    event.preventDefault();
    
    let formData = new FormData(this);
    let vacancies = [];
    
    document.querySelectorAll('.col-6').forEach(function(card) {
    
    let vacancy = {};
    card.querySelectorAll('input[type=text], textarea').forEach(function(input) {
        vacancy[input.name] = input.value;
    });
    vacancies.push(vacancy);
    });

    formData.append('vacancies', JSON.stringify(vacancies));

    formData.delete('vacancyName')
    formData.delete('vacancyDescription')
    formData.delete('vacancyNeeds')
    formData.delete('vacancyTags')

    console.log(formData)
    fetch(window.location.href, {
        method: 'POST',
        body: formData
    })
    .then(respone => {
        if(respone.ok){
            return respone.json()
        }
    })
    .then(data => {
        window.location.href = data.url
    })

})


function showNotification(message, color) {  // for base_template.html
    var notification = $('<div class="alert alert-' + color + ' alert-dismissible fade show" role="alert">' +
      message +
      '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Закрыть"></button>' +
      '</div>');

    $('#notification-container').append(notification);

    setTimeout(function() {
      notification.alert('close');
    }, 5000);
  }

function show_spinner(){
    document.getElementById('spinner').style.display = 'flex';
    document.getElementsByTagName('body')[0].style.overflow = 'hidden'
}

function hide_spinner(){
    document.getElementById('spinner').style.display = 'none';
        document.getElementsByTagName('body')[0].style.overflow = 'auto'

}

