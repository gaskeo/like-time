function showResult() {
    let link_or_username = document.getElementById("account-link-input")

    if (!(link_or_username.value.replace(/\s/g, '').length)) {
        link_or_username.placeholder = "впиши в меня что-нибудь пожалуйста..."
        link_or_username.value = ""
        return
    }
    let form = new FormData()
    form.append("link_or_username", link_or_username.value)
    fetch("/do_search", {method: 'post', body: form}).then(function (r) {
            let status = r.status

            if (status === 200) {
                r.json().then(function (j) {
                    if (j["status"] !== "ok") {
                        alert("no...")
                    } else {
                        alert("ok")
                    }
                })
            } else {
                alert(status);
            }
        }
    )
}
