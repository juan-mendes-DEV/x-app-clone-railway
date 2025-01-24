function likePost(postId, button) {
    fetch(`/like/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({}) // Corpo vazio, só enviamos o ID do post
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Like removed.") {
            button.innerHTML = `Curtir (${data.likes_count})`;
            button.classList.remove("liked");
        } else if (data.message === "Post liked.") {
            button.innerHTML = `Curtido (${data.likes_count})`;
            button.classList.add("liked");
        }
    })
    .catch(error => console.error('Erro ao curtir o post:', error))
    .finally(() => {
        button.disabled = false; // Habilita o botão novamente
    });
}

// Função auxiliar para obter o CSRF token
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    console.warn('CSRF token não encontrado!');
    return '';
}

document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.getAttribute('data-post-id');
            button.disabled = true; // Desativa o botão temporariamente
            likePost(postId, button);
        });
    });
});

