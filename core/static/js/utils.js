var d = document.querySelectorAll('.from-now')
for (i=0; i < d.length; i++){
	var v = d[i].getAttribute('data-val');
	d[i].textContent = moment(v).fromNow();
}

