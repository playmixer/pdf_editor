links = document.getElementsByName('nav_link')
for (var i = 0; i <= links.length; i++) {
  if (document.location.pathname === links[i]?.pathname) {
    links[i].classList.add('active')
  }
}
