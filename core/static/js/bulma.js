
	//burger
	var burger = document.querySelector('.burger');
	var menu = document.querySelector('#' + burger.dataset.target);

	burger.addEventListener('click', function() {
		burger.classList.toggle('is-active')
		menu.classList.toggle('is-active')
	});

	//notifications
	document.addEventListener('DOMContentLoaded', () => {
	  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
	    $notification = $delete.parentNode;
	    $delete.addEventListener('click', () => {
	      $notification.parentNode.removeChild($notification);
	    });
	  });
	});
