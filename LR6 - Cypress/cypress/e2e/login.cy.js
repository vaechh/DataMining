describe('Авторизация в почте', () => {
  it('Выполнить вход и сохранить cookies', () => {
    cy.visit('https://mail.psu.ru/');

    // Логин
    cy.get('input[name="Username"]').type('vaechh');
    cy.get('input[name="Password"]').type('JohnVae322');
    cy.get('input[type="submit"][name="login"][value="Войти"]').click();

    // Сохранить cookies после входа
    cy.getCookies().should('have.length.greaterThan', 0).then((cookies) => {
      window.localStorage.setItem('mailCookies', JSON.stringify(cookies));
    });
  });
});
