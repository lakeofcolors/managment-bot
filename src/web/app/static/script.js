var own_url = window.location.href
var url_obj = new URL(own_url);
var dashboard_id = url_obj.searchParams.get("dashboard_id");

var dashboard;
var tasks;

var url = "http://localhost/api/dashboard/"

fetch(url.concat(dashboard_id))
  .then(response => response.json())
  .then(data => {
    dashboard_title = document.getElementById("dashboard_id");
    dashboard_title.innerHTML = data.name;
  });


fetch("http://localhost/api/tasks/dashboard/1")
  .then(response => response.json())
  .then(data => {
    data.forEach(function(item, index, array) {
      var task_obj = document.getElementById(item.status);
      console.log(task_obj)
      var tag = document.createElement("p");
      tag.innerText = item.name
      task_obj.appendChild(tag);
      console.log(item, index);
    });
  });
