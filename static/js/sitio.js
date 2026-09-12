// Guion del sitio. Vive aqui y no incrustado en la pagina para que la politica
// de contenido pueda prohibir los guiones en linea, que es por donde llega casi
// todo ataque de inyeccion.
//
// Es corto a proposito: la pagina se lee sin JavaScript. Lo unico que hace
// falta es el menu del telefono; las preguntas se pliegan solas con <details>.

document.addEventListener('DOMContentLoaded', () => {
  const boton = document.querySelector('[data-abre-menu]');
  const menu = document.getElementById('menu-telefono');
  if (!boton || !menu) return;

  boton.addEventListener('click', () => {
    const abierto = menu.hasAttribute('hidden');
    if (abierto) {
      menu.removeAttribute('hidden');
    } else {
      menu.setAttribute('hidden', '');
    }
    boton.setAttribute('aria-expanded', String(abierto));
  });

  // Al elegir una seccion, el menu se cierra: en un telefono tapa la pagina.
  menu.addEventListener('click', (evento) => {
    if (evento.target.closest('a')) {
      menu.setAttribute('hidden', '');
      boton.setAttribute('aria-expanded', 'false');
    }
  });
});
