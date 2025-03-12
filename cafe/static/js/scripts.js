document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-item');
    const totalForms = document.getElementById('id_items-TOTAL_FORMS');
    const container = document.getElementById('order-items');

    // Добавляем обработчик для кнопок добавления
    addButton.addEventListener('click', function() {
        const formCount = parseInt(totalForms.value);
        const newForm = document.querySelector('.order-item-form').cloneNode(true);

        // Замена индексов
        newForm.innerHTML = newForm.innerHTML.replace(
            /orderitem_set-(\d+)-/g,
            `orderitem_set-${formCount}-`
        );

        // Очистка значений
        newForm.querySelector('.dish-select').selectedIndex = 0;
        newForm.querySelector('input[type="number"]').value = 1;

        container.appendChild(newForm);
        totalForms.value = formCount + 1; // Обновляем TOTAL_FORMS
    });

    // Добавляем кнопки удаления к существующим формам
    document.querySelectorAll('.order-item-form').forEach(form => {
        addRemoveButton(form);
    });

    // Добавляем обработчик для кнопок удаления
    container.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-form')) {
            e.preventDefault();
            const formWrapper = e.target.closest('.order-item-form');
            const deleteCheckbox = formWrapper.querySelector('input[type="checkbox"][name$="-DELETE"]');
            const formCount = parseInt(totalForms.value);

            if (deleteCheckbox) {
                // Если форма уже существует в БД, помечаем на удаление
                deleteCheckbox.checked = true;
                formWrapper.style.display = 'none';
            } else {
                // Если форма новая, удаляем полностью
                formWrapper.remove();
                totalForms.value = formCount - 1; // Обновляем TOTAL_FORMS
            }
        }
    });



});


// Функция добавления кнопки удаления
function addRemoveButton(formWrapper) {
    const removeButton = document.createElement('button');
    removeButton.textContent = '×';
    removeButton.className = 'remove-form';
    removeButton.style.cssText = `
        position: absolute;
        right: 10px;
        top: 10px;
        background: red;
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
    `;

    formWrapper.style.position = 'relative';
    formWrapper.appendChild(removeButton);
}