var own_url = window.location.href
var url_obj = new URL(own_url);
var dashboard_id = url_obj.searchParams.get("dashboard_id");
var dashboard;
var tasks;

var url = "https://lakeofcolors.com/api/dashboard/"

function create_task() {
  var name = document.getElementById("name");
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({name: name.value,
                          dashboard_id: dashboard_id,
                          status: 'no_status'
                         })
  }
  fetch("https://lakeofcolors.com/api/tasks/create", requestOptions)
    .then(response => response.json())
    // .then(data => alert("create task"))
  location.reload();
}


function change_state(status, task_id) {

  const requestOptions = {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: status})
  }
  fetch("https://lakeofcolors.com/api/tasks/".concat(task_id), requestOptions)
    .then(response => response.json())
    // .then(data => alert("state change"))
  location.reload();
}



fetch(url.concat(dashboard_id))
  .then(response => response.json())
  .then(data => {
    dashboard_title = document.getElementById("dashboard_id");
    dashboard_title.innerHTML = data.name;
  });


fetch("https://lakeofcolors.com/api/tasks/dashboard/".concat(dashboard_id))
  .then(response => response.json())
  .then(data => {
    data.forEach(function(item, index, array) {
      var task_obj = document.getElementById(item.status);
      var tag = document.createElement("p");
      tag.innerText = item.name
      task_obj.appendChild(tag);

      var statuses = ['no_status', 'todo', 'in_progress', 'done']
      statuses.forEach(function(status) {
        var btn = document.createElement("button")
        btn.innerText = "move to ".concat(status);
        btn.addEventListener('click', function handleClick(event){
          // console.log(event);
          change_state(status, item.id)
        });
        task_obj.appendChild(btn);
      });

    });
  });

