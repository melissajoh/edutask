describe('Manipulate todo list associated to a task', () => {
    let uid
    let name
    let email
    let task = {
        "title": "Task 1",
        "description": "Description of task 1"
    }
    let todo = {
        "description": "Description of todo item"
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
        })
    })

    beforeEach(function () {
        cy.visit('http://localhost:3000')

        //login
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)

        cy.get('form')
            .submit()

        // add task
        cy.contains('div', 'Title')
            .find('input[type=text]')
            .type(task.title)

        cy.get('form')
            .submit()

        // click on task
        cy.contains('div', 'Task 1').click()
    })

    it('clicking add with filled in description should create todo item', () => {
        cy.get('.inline-form')
            .find('input[type=text]')
            .type(todo.description)

        cy.get('.inline-form')
            .submit()

        cy.get('.editable').eq(3).contains(todo.description)
    })

    it('clicking add with empty description should not be possible', () => {
        cy.get('.inline-form')
            .find('input[type=submit]')
            // .should('be.disabled')
    })

    it('clicking checker icon should set item to done and struck through if active', () => {
        cy.get('.checker').eq(1).should('have.class', 'unchecked')
        cy.get('.checker').eq(1).click()
        cy.get('.checker').eq(1).should('have.class', 'checked')
        cy.get('.editable').eq(3)
            .invoke('css', 'text-decoration')
            .should('contain', 'line-through')
    })

    it('clicking checker icon should set item to active and not struck through if done', () => {
        cy.get('.checker').eq(1).click()
        cy.get('.checker').eq(1).should('have.class', 'unchecked')
        cy.get('.editable').eq(3)
            .invoke('css', 'text-decoration')
            .should('not.contain', 'line-through')
    })

    it('item should be deleted if clicking X symbol', () => {
        cy.get('.remover').eq(1).click()
        cy.get('.remover').eq(1).should('not.exist')
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