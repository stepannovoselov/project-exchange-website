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


function change_password_request(){  // for account-profile.html
    let form = new FormData()

    let oldPassword = document.getElementById('oldPassword')
    let newPassword = document.getElementById('newPassword')

    form.append('oldPassword', oldPassword.value)
    form.append('newPassword', newPassword.value)

    fetch(window.location.href + 'password', {
        method: 'POST',
        body: form
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        if (data.errors){
            let errorMessages = Object.values(data.errors).flat();
            let errorMessageString = '● ' + errorMessages.join('<br>● ');
            showNotification('Ошибка при изменении пароля!<br>' + errorMessageString, 'danger')
        }
        else{
            oldPassword.value = ''
            newPassword.value = ''
            showNotification('Пароль успешно изменён.', 'success')
        }
        close_password_modal()
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
        close_ai_modal()
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
        close_ai_modal()
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
        close_ai_modal()
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
        close_ai_modal();
    })
}


function close_ai_modal() {
    let ai_tools_modal = document.getElementById('AI_tools')

    $(ai_tools_modal).modal('hide');
}

function close_password_modal(){
    let password_modal = document.getElementById('changePasswordModal')

    $(password_modal).modal('hide');
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
    
    document.getElementById('vacancyCards').querySelectorAll('.col-6').forEach(function(card) {
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


    let team_container = document.getElementById('team-container')
    let teammate_usernames = []
    team_container.querySelectorAll('li').forEach(function(teammate) {
        teammate_usernames.push(teammate.id)
    })

    formData.append('teammates', JSON.stringify(teammate_usernames))

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


function search_users_request(){  // for create-project-form.html
    let search_users = document.getElementById('search_users')
    let users_list = document.getElementById('users_list')

    fetch('/account/users?' + new URLSearchParams({
        'query': search_users.value,
        'except_me': true
    }), {
        method: 'GET',
    })
    .then((respone) => {
        return respone.json()
    })
    .then((data) => {
        while (users_list.firstChild) {
            users_list.removeChild(users_list.firstChild);
        }
        data.forEach(user => {
            users_list.innerHTML += '<li><a style="cursor: pointer" class="dropdown-item" onclick="add_user_to_project_team(\'' + user.username + '\', \'' +  user.surname + '\', \'' + user.name + '\')">' + user.surname + ' ' + user.name + ' ' + '(@' + user.username + ')' + '</a></li>'
        });
    })
}
search_users_request()


function add_user_to_project_team(username, user_surname, user_name){
    let team_container = document.getElementById('team-container')

    team_container.innerHTML += '<li id=' + username + ' onclick="this.parentNode.removeChild(this)" style="cursor: pointer"><div>' + user_surname + ' ' + user_name + ' ' + '(@' + username + ')' + ' <svg width="30px" height="30px" viewBox="0 -0.5 25 25" stroke="#ff0000" xmlns="http://www.w3.org/2000/svg"><path d="M6.96967 16.4697C6.67678 16.7626 6.67678 17.2374 6.96967 17.5303C7.26256 17.8232 7.73744 17.8232 8.03033 17.5303L6.96967 16.4697ZM13.0303 12.5303C13.3232 12.2374 13.3232 11.7626 13.0303 11.4697C12.7374 11.1768 12.2626 11.1768 11.9697 11.4697L13.0303 12.5303ZM11.9697 11.4697C11.6768 11.7626 11.6768 12.2374 11.9697 12.5303C12.2626 12.8232 12.7374 12.8232 13.0303 12.5303L11.9697 11.4697ZM18.0303 7.53033C18.3232 7.23744 18.3232 6.76256 18.0303 6.46967C17.7374 6.17678 17.2626 6.17678 16.9697 6.46967L18.0303 7.53033ZM13.0303 11.4697C12.7374 11.1768 12.2626 11.1768 11.9697 11.4697C11.6768 11.7626 11.6768 12.2374 11.9697 12.5303L13.0303 11.4697ZM16.9697 17.5303C17.2626 17.8232 17.7374 17.8232 18.0303 17.5303C18.3232 17.2374 18.3232 16.7626 18.0303 16.4697L16.9697 17.5303ZM11.9697 12.5303C12.2626 12.8232 12.7374 12.8232 13.0303 12.5303C13.3232 12.2374 13.3232 11.7626 13.0303 11.4697L11.9697 12.5303ZM8.03033 6.46967C7.73744 6.17678 7.26256 6.17678 6.96967 6.46967C6.67678 6.76256 6.67678 7.23744 6.96967 7.53033L8.03033 6.46967ZM8.03033 17.5303L13.0303 12.5303L11.9697 11.4697L6.96967 16.4697L8.03033 17.5303ZM13.0303 12.5303L18.0303 7.53033L16.9697 6.46967L11.9697 11.4697L13.0303 12.5303ZM11.9697 12.5303L16.9697 17.5303L18.0303 16.4697L13.0303 11.4697L11.9697 12.5303ZM13.0303 11.4697L8.03033 6.46967L6.96967 7.53033L11.9697 12.5303L13.0303 11.4697Z" fill="#ff0000"/></svg></div></li>'
}