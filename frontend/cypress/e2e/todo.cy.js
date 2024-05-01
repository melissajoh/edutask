describe('Manipulate todo list associated to a task', () => {
    let uid
    let name
    let email
    let task = {
        "title": "Task 1",
        "description": "Description of task 1"
    }
    let todo = {
        "description": "Added todo item"
    }
    let setup = {
        "description": "Setup todo item"
    }

    before(function () {
    // user setup
    cy.fixture('user.json')
        .then((user) => {
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            form: true,
            body: user
        }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
            email = user.email
        })

        cy.visit('http://localhost:3000')

        //login
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(user.email)

        cy.get('form')
            .submit()

        // add task
        cy.contains('div', 'Title')
            .find('input[type=text]')
            .type(task.title)

        cy.get('form')
            .submit()
        })

        // add todo item
        cy.contains('div', 'Task 1').click()
        cy.get('.inline-form')
        .find('input[type=text]')
        .type(setup.description)

        cy.get('.inline-form')
            .submit()
    })

    beforeEach(function () {
        cy.viewport(1280, 1000)
        cy.visit('http://localhost:3000')

        // login
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)

        cy.get('form')
            .submit()

        // detail view for task 1
        cy.contains('div', 'Task 1').click()
    })

    it('clicking add with filled in description should create todo item', () => {
        cy.get('.inline-form')
            .find('input[type=text]')
            .type(todo.description)

        cy.get('.inline-form')
            .submit()

        cy.contains(todo.description).should('exist')
    })

    it('clicking add with empty description should not be possible', () => {
        cy.get('.inline-form')
            .find('input[type=submit]')
            .should('be.disabled')
    })

    it('clicking checker icon should set item to done and struck through if active', () => {
        cy.contains(setup.description).parent().get('.checker').should('have.class', 'unchecked')
        cy.contains(setup.description).parent().find('.checker').click()
        cy.contains(setup.description).parent().get('.checker').should('have.class', 'checked')
        cy.contains(setup.description)
            .invoke('css', 'text-decoration')
            .should('contain', 'line-through')
        cy.contains(setup.description).parent().find('.checker').click()
    })

    it('clicking checker icon should set item to active and not struck through if done', () => {
        cy.contains(setup.description).parent().find('.checker').click()
        cy.contains(setup.description).parent().find('.checker').click()
        cy.contains(setup.description).parent().find('.checker').should('have.class', 'unchecked')
        cy.contains(setup.description)
            .invoke('css', 'text-decoration')
            .should('not.contain', 'line-through')
    })

    it('item should be deleted if clicking X symbol', () => {
        cy.get('.inline-form')
            .find('input[type=text]')
            .type('delete me')

        cy.get('.inline-form')
            .submit()

        cy.contains('delete me').parent().find('.remover').click()
        cy.contains('delete me').parent().find('.remover').click()
        cy.contains('delete me').should('not.exist')
    })

    after(function () {
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})