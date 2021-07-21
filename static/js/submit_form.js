function showResult() {
    let link_or_username = document.getElementById("account-link-input")

    if (!(link_or_username.value.replace(/\s/g, '').length)) {
        link_or_username.placeholder = "впиши в меня что-нибудь пожалуйста..."
        link_or_username.value = ""
        return
    }
    let form = new FormData()
    form.append("shortcode_or_link", link_or_username.value)
    document.getElementById("loading").style.display = "block"
    document.getElementById("send-button").disabled = true
    if (document.getElementById("table-likes")) {
        document.getElementById("table-likes").remove()
    }
    fetch("/do_search", {method: 'post', body: form}).then(function (r) {
            let status = r.status

            if (status === 200) {
                r.json().then(function (j) {
                    if (j["answer"] !== "ok") {
                        alert(j["answer"])
                    } else {
                        let width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
                        document.getElementById("loading").style.display = "none"
                        let table = document.createElement("table")
                        table.id = "table-likes"
                        let row = document.createElement("tr")
                        row.appendChild(document.createElement("th"))
                        for (let i = 1; i < j["posts"].length + 1; i++) {
                            let post_cell = document.createElement("th")
                            let post_link = document.createElement("a")
                            post_link.href = "https://instagram.com/p/" + j["posts"][i - 1]
                            let plus
                            if (width > 999) {
                                plus = "пост "
                            } else plus = ""
                            let link_text = document.createTextNode(plus + i.toString())

                            post_link.title = i.toString()
                            post_link.appendChild(link_text)
                            post_cell.appendChild(post_link)
                            row.appendChild(post_cell)
                        }
                        table.appendChild(row)
                        let refactored_data = mapToArray(j["users"])
                        refactored_data.sort(function (a, b) {
                            return b[1].length - a[1].length || a[0].localeCompare(b[0])
                        })
                        for (let i = 0; i < refactored_data.length; i++) {
                            let row = document.createElement("tr")
                            let user = document.createElement("th")
                            let user_link = document.createElement("a")
                            user_link.href = "https://instagram.com/" + refactored_data[i][0]
                            let link_text = document.createTextNode(refactored_data[i][0])
                            user_link.title = refactored_data[i][0]
                            user_link.appendChild(link_text)
                            user.appendChild(user_link)
                            user.className = "user-th"
                            row.appendChild(user)
                            let likes = refactored_data[i][1]
                            for (let post = 0; post < 10; post++) {
                                let like = document.createElement("th")
                                if (likes.includes(post)) {
                                    like.textContent = '\u2764'
                                    like.className = "heart"
                                }
                                row.appendChild(like)

                            }
                            table.appendChild(row)
                        }
                        loading.after(table)
                        document.getElementById("send-button").disabled = false

                    }
                })
            } else {
                alert(status);
                document.getElementById("loading").style.display = "none"
                document.getElementById("send-button").disabled = false

            }
        }
    )
}

function mapToArray(map) {
    let keys = Object.keys(map)
    let array = []
    for (let i = 0; i < keys.length; i++) {
        array.push([keys[i], map[keys[i]]])
    }
    return array
}