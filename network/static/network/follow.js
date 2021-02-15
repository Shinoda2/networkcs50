document.addEventListener('DOMContentLoaded', function (){

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
    const csrftoken = getCookie('csrftoken');
    
    console.log('hola')
    follow_btn = document.querySelector("#follow-btn");
    follow_btn.addEventListener("click", (e) => {
    user = follow_btn.getAttribute("data-user");
    action = follow_btn.textContent.trim();
    form = new FormData();
    form.append("user", user);
    form.append("action", action);
    fetch("/follow/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrftoken,
          },
        body: form,
    })
    .then((res) => res.json())
    .then((res) => {
        console.log('presionado')
      if (res.status == 201) {
        follow_btn.textContent = res.action;
        document.querySelector(
          "#follower"
        ).textContent = `Followers ${res.follower_count}`;
      }
    })
})
});
