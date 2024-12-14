/*=============== SHOW SIDEBAR ===============*/
const showSidebar = (toggleId, sidebarId, mainId) => {
    const toggle = document.getElementById(toggleId),
        sidebar = document.getElementById(sidebarId),
        main = document.getElementById(mainId)

    if (toggle && sidebar && main) {
        toggle.addEventListener('click', () => {
            /* Show sidebar */
            sidebar.classList.toggle('show-sidebar')
                /* Add padding main */
            main.classList.toggle('main-pd')
        })
    }
}
showSidebar('header-toggle', 'sidebar', 'main')

/*=============== LINK ACTIVE ===============*/
const sidebarLink = document.querySelectorAll('.sidebar__link')

function linkColor() {
    sidebarLink.forEach(l => l.classList.remove('active-link'))
    this.classList.add('active-link')
}

sidebarLink.forEach(l => l.addEventListener('click', linkColor))

document.querySelectorAll('.sidebar__link.dropdown').forEach(dropdown => {
    dropdown.addEventListener('click', () => {
        dropdown.classList.toggle('active');
    });
});
/*=============== LINK ACTIVE ===============*/
let swiperFeatured = new Swiper('.featured__swiper', {
    loop: true,
    spaceBetween: 16,
    grapCursor: true,
    slidesPerView: 'auto',
    centeredSlides: 'auto',

    breakpoints: {
        1150: {
            slidesPerView: 3,
            centeredSlides: false,
        }
    }
})
let swiperFeatured2 = new Swiper('.featured__swiper2', {
    loop: true,
    spaceBetween: 16,
    grapCursor: true,
    slidesPerView: 'auto',
    centeredSlides: 'auto',

    breakpoints: {
        1150: {
            slidesPerView: 3,
            centeredSlides: false,
        }
    }
})
let swiperTestimonial = new Swiper('.testimonial__swiper', {
    loop: true,
    spaceBetween: 16,
    grapCursor: true,
    slidesPerView: 'auto',
    centeredSlides: 'auto',

    breakpoints: {
        1150: {
            slidesPerView: 3,
            centeredSlides: false,
        }
    }
})


function changeImage(imageSrc, detailsId) {
    // تحديث الصورة الرئيسية
    const mainImage = document.getElementById("mainImage");
    mainImage.src = imageSrc;

    // إخفاء جميع النصوص
    const allDetails = document.querySelectorAll(".details");
    allDetails.forEach((detail) => {
        detail.style.display = "none";
    });

    // إظهار النصوص المرتبطة بالصورة
    const selectedDetails = document.getElementById(`details-${detailsId}`);
    if (selectedDetails) {
        selectedDetails.style.display = "block";
    }
}
// دالة زيادة الكمية
function increaseQuantity() {
    const quantityInput = document.getElementById("quantity");
    let currentValue = parseInt(quantityInput.value, 10); // تحويل القيمة الحالية إلى رقم
    quantityInput.value = currentValue + 1; // زيادة الكمية بمقدار 1
}

// دالة تقليل الكمية
function decreaseQuantity() {
    const quantityInput = document.getElementById("quantity");
    let currentValue = parseInt(quantityInput.value, 10); // تحويل القيمة الحالية إلى رقم
    if (currentValue > 0) {
        quantityInput.value = currentValue - 1; // تقليل الكمية بمقدار 1 إذا كانت الكمية أكبر من 0
    }
}


/*=============== SHOW HIDDEN - PASSWORD ===============*/
// const showHiddenPass = (loginPass, loginEye) => {
//     const input = document.getElementById(loginPass), // الحصول على حقل كلمة السر
//         iconEye = document.getElementById(loginEye); // الحصول على أيقونة العين

//     iconEye.addEventListener('click', () => { // إضافة حدث عند النقر على الأيقونة
//         if (input.type === 'password') { // إذا كانت كلمة السر مخفية
//             input.type = 'text'; // تغييرها إلى نص (إظهار كلمة السر)
//             iconEye.classList.add('ri-eye-line'); // تغيير الأيقونة إلى العين المفتوحة
//             iconEye.classList.remove('ri-eye-off-line'); // إزالة الأيقونة المغلقة
//         } else {
//             input.type = 'password'; // إعادة كلمة السر إلى مخفية
//             iconEye.classList.remove('ri-eye-line'); // إعادة الأيقونة إلى العين المغلقة
//             iconEye.classList.add('ri-eye-off-line'); // إضافة الأيقونة المغلقة
//         }
//     });
// }

// showHiddenPass('login-pass', 'login-eye'); // استدعاء الدالة مع المعرفات المناسبة