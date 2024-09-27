fetch('/')
    .then(response => {
        if (!response.ok){
            throw new Error("Erro ao carregar formulários");
        }
        return response.json();
    })
    .then(forms => {
        const formList = document.getElementById('form-list');
        forms.forEach(form => {
            const listItem = document.createElement('li');
            listItem.textContent = form.title;
            formList.appendChild(listItem);
            
        });
    })
    .catch(error => {
        console.error("Erro ao carregar formulários: ", error);
    });