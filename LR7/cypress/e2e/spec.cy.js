describe('Автоматизация входа и чтения писем', () => {
  beforeEach(() => {
    // Игнорируем ошибку getCrystalOpenNodes не найдено
    Cypress.on('uncaught:exception', (err, runnable) => {
      // Игнорировать ошибку, если это связано с getCrystalOpenNodes
      if (err.message.includes('getCrystalOpenNodes is not defined')) {
        return false; // предотвращаем фейл теста
      }
      // Для всех других ошибок все равно позволим Cypress их поймать
      return true;
    });
  });

  it('Авторизация и чтение содержимого писем', () => {
    const emails = []; // Массив для хранения данных о письмах

    // Переход на страницу почты
    cy.visit('https://mail.psu.ru/');

    // Логин
    cy.get('input[name="Username"]').type('');
    cy.get('input[name="Password"]').type('');
    cy.get('input[type="submit"][name="login"][value="Войти"]').click();

    // Ожидание загрузки списка писем
    cy.get("tr.borderbottom", { timeout: 10000 }).should('have.length.greaterThan', 0);

    // Чтение первых 5 писем
    cy.get("tr.borderbottom").each(($row, index) => {
      if (index < 5) { // Ограничиваем количество писем
        cy.log(`Открываем письмо ${index + 1}`);
        cy.wait(5000);
        // Перезапрашиваем строку письма перед кликом
        cy.get("tr.borderbottom").eq(index).as('emailRow');

        // Клик по i-му письму
        cy.get('@emailRow').find("td").eq(-3).find("a").click();

        // Ожидание загрузки содержимого письма
        cy.get("h2.msgSubject.padRight", { timeout: 10000 }).should('exist');  // Проверяем, что заголовок письма доступен
        cy.wait(5000);

        // Извлечение заголовка письма
        cy.get("h2.msgSubject.padRight")
          .invoke('text')
          .then((subjectText) => {
            cy.log(`Заголовок письма: ${subjectText}`);
            const cleanedSubject = subjectText.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();

            // Извлечение метаданных (от кого, дата, кому)
            cy.get("div.msgHeaders p.msgHeader")
              .then(($headers) => {
                const headers = $headers.map((_, el) => Cypress.$(el).text()).get();

                const fromMatch = headers[0].match(/От Кого:\s*(.*)/);
                const dateMatch = headers[1].match(/Дата:\s*(.*)/);

                const fromEmail = fromMatch ? fromMatch[1] : null;
                const dateSent = dateMatch ? dateMatch[1] : null;

                cy.log(`От кого: ${fromEmail}`);
                cy.log(`Дата отправки: ${dateSent}`);

                // Сохранение данных в массив
                emails.push({
                  subject: cleanedSubject,
                  from: fromEmail,
                  date: dateSent
                });

                // Сохранение данных в JSON файл после всех писем
                if (index === 4) {
                  cy.writeFile('cypress/fixtures/emails.json', emails);
                }
              });
          });

        // Возврат к списку писем
        cy.go('back');

        // Ожидание того, что список писем снова будет доступен
        cy.get("tr.borderbottom", { timeout: 10000 }).should('have.length.greaterThan', 0);

        // Перезапрашиваем строку письма с правильным индексом, чтобы кликнуть на нужное
        cy.get("tr.borderbottom").eq(index).as('emailRow');  // Перезапрашиваем строки
      }
    });
  });
});
