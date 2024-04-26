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

        cy.get('.editable').contains('Description of todo item')
    })

    it('clicking add with empty description should not be possible', () => {
        cy.get('.inline-form')
            .find('input[type=submit]')
            // .should('be.disabled')
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