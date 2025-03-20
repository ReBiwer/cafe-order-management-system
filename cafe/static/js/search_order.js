document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    let timeoutId;

    searchInput.addEventListener('input', (e) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            performSearch(e.target.value);
        }, 300);
    });

    async function performSearch(query) {
        try {
            const url = urlSearchOrder  + '?value_search=' + query
            const response = await fetch(url);
            if (!response.ok) throw new Error('HTTP error');
            const data = await response.json();
            updateOrdersList(data);
        } catch (error) {
            console.error('Ошибка поиска:', error);
            showError();
        }
    }

    function updateOrdersList(orders) {
        const container = document.getElementById('ordersContainer');

        // Очищаем контейнер перед добавлением новых данных
        container.innerHTML = '';

        if (orders.length === 0) {
            container.innerHTML = '<p class="no-results">Ничего не найдено</p>';
            return;
        }

        // Создаем HTML для каждого заказа
        orders.forEach(order => {
            const orderCard = document.createElement('div');
            orderCard.className = 'order-card';

            // Основная информация о заказе
            orderCard.innerHTML = `
                <h3><a href=${order.url}>Заказ №${order.id}</a></h3>
                <h4>Стол № ${order.table_number}</h4>
                <p>Статус: ${order.status}</p>
                <p>Сумма: ${order.total_price} ₽</p>

                <table class="bordered-table">
                    <thead>
                      <tr>Позиции</tr>
                      <tr>
                        <th>Блюдо</th>
                        <th>Кол-во</th>
                        <th>Цена</th>
                      </tr>
                    </thead>
                </table>
            `;

            // Добавляем элементы заказа (OrderItem)
            const itemsList = orderCard.querySelector('.bordered-table');
            order.items.forEach(item => {
                const itemElement = document.createElement('tr');
                itemElement.className = 'order-item';
                itemElement.innerHTML = `
                    <th>${item.dish.name}</th>
                    <th>${item.quantity}</th>
                    <th>${item.price}</th>
                `;
                itemsList.appendChild(itemElement);
            });

            // Добавляем карточку заказа в контейнер
            container.appendChild(orderCard);
        });
    }

    function showError() {
        document.getElementById('ordersContainer').innerHTML =
            '<div class="alert alert-danger">Ошибка загрузки данных</div>';
    }

});
