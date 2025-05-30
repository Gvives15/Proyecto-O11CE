// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebarClose = document.getElementById('sidebar-close');
    const sidebar = document.getElementById('sidebar');
    const appWrapper = document.querySelector('.app-wrapper');
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.dropdown-menu');
    const alertMessage = document.getElementById('alert-message');
    
    // Initialize submenu handlers
    initSubmenuHandlers();
  
    // Toggle sidebar on desktop
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', () => {
        // En pantallas grandes, toggle el colapso
        if (window.innerWidth > 768) {
          appWrapper.classList.toggle('sidebar-collapsed');
          
          // Save preference to localStorage
          const isCollapsed = appWrapper.classList.contains('sidebar-collapsed');
          localStorage.setItem('sidebar-collapsed', isCollapsed);
        } 
        // En pantallas pequeñas, muestra la barra lateral completa
        else {
          // Asegurarse de que la barra lateral NO esté colapsada en móvil
          appWrapper.classList.remove('sidebar-collapsed');
          sidebar.classList.add('show');
        }
      });
    }
  
    // Close sidebar on mobile
    if (sidebarClose) {
      sidebarClose.addEventListener('click', () => {
        sidebar.classList.remove('show');
      });
    }
  
    // Toggle dropdown menu
    if (dropdownToggle) {
      dropdownToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownMenu.classList.toggle('show');
      });
    }
  
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (dropdownToggle && dropdownMenu && 
          !dropdownToggle.contains(e.target) && 
          !dropdownMenu.contains(e.target)) {
        dropdownMenu.classList.remove('show');
      }
    });
  
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 768 && 
          sidebar && 
          !sidebar.contains(e.target) && 
          !sidebarToggle.contains(e.target) &&
          sidebar.classList.contains('show')) {
        sidebar.classList.remove('show');
      }
    });
  
    // Auto-hide alert messages after 6 seconds
    if (alertMessage) {
      setTimeout(() => {
        alertMessage.style.display = 'none';
      }, 6000);
    }
  
    // Check for saved sidebar state (solo en desktop)
    if (window.innerWidth > 768) {
      const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
      if (isCollapsed) {
        appWrapper.classList.add('sidebar-collapsed');
      }
    } else {
      // En móvil, siempre asegurarse de que no esté colapsada
      appWrapper.classList.remove('sidebar-collapsed');
    }
  });
  
  // Toggle submenu function
  function initSubmenuHandlers() {
    // Get all links with submenu
    const submenuLinks = document.querySelectorAll('.nav-link.has-submenu');
    
    // Add click event to each submenu link
    submenuLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Get the submenu ID from data attribute
        const submenuId = this.getAttribute('data-submenu');
        const submenu = document.getElementById(submenuId);
        
        // Toggle expanded class on submenu
        if (submenu) {
          // Close all other submenus first
          document.querySelectorAll('.submenu.expanded').forEach(menu => {
            // Skip the current submenu
            if (menu.id !== submenuId) {
              menu.classList.remove('expanded');
              // Find the associated link and remove expanded class
              const parentLink = document.querySelector(`[data-submenu="${menu.id}"]`);
              if (parentLink) {
                parentLink.classList.remove('expanded');
              }
            }
          });
          
          // Toggle current submenu
          submenu.classList.toggle('expanded');
          this.classList.toggle('expanded');
        }
      });
    });
    
    // Check if there's an active submenu item to expand its parent
    const activeSubmenuItem = document.querySelector('.submenu-link.active');
    if (activeSubmenuItem) {
      const parentSubmenu = activeSubmenuItem.closest('.submenu');
      if (parentSubmenu) {
        parentSubmenu.classList.add('expanded');
        const parentLink = document.querySelector(`[data-submenu="${parentSubmenu.id}"]`);
        if (parentLink) {
          parentLink.classList.add('expanded');
        }
      }
    }
  }
  
  // Handle window resize
  window.addEventListener('resize', () => {
    const sidebar = document.getElementById('sidebar');
    const appWrapper = document.querySelector('.app-wrapper');
    
    if (window.innerWidth > 768) {
      // En desktop
      sidebar.classList.remove('show');
      // Restaurar el estado guardado
      const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
      if (isCollapsed) {
        appWrapper.classList.add('sidebar-collapsed');
      }
    } else {
      // En móvil, siempre asegurarse de que no esté colapsada
      appWrapper.classList.remove('sidebar-collapsed');
    }
  });