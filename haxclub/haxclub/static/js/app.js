console.log("                                      ")
console.log("          _____         _             ")
console.log("         |_   _| ___  _| | ___        ")
console.log("           | |  | . || . || . |       ")
console.log("           |_|  |___||___||___|       ")
console.log("                                      ")
console.log("              John Salvatore          ")

//App
/*==================================================*/
App = Ember.Application.create({
    currentPath: '',
});
/*==================================================*/

//Adapter
/*==================================================*/
App.ApplicationAdapter = DS.DjangoRESTAdapter.extend({
    namespace: 'todo/api',
});
/*==================================================*/

//Serializer
/*==================================================*/
App.ApplicationSerializer = DS.DjangoRESTSerializer.extend();
/*==================================================*/

//Models
/*==================================================*/
var args;
App.Todo = DS.Model.extend({
    data: DS.attr(),

    // helper method to handle getting amd setting of 
    // computed properties via the JSON data attribute
    getOrSet: function(key,value){
        var data = this.get('data');
        if (value === undefined){
            return data[key];
        }else{
            data[key] = value;
            this.set('data',data);
            this.save()
            return value
        }
    },

    title: function(key,value,oldValue){
        return this.get('data')[key];
    }.property('data'),

    isCompleted: function(key,value,oldValue){
        return this.getOrSet(key,value);
    }.property('data'),
});
/*==================================================*/

//Router
/*==================================================*/
App.Router.map(function(){
    this.resource('todos', {path: '/'}, function(){
        this.route('active');
        this.route('completed');
    });
});
/*==================================================*/

//Routes
/*==================================================*/
App.TodosRoute = Ember.Route.extend({
    model: function(){
        return this.store.find('todo');
    },
});

App.TodosIndexRoute = Ember.Route.extend({
    model: function(){
        return this.modelFor('todos');
    },
});

App.TodosActiveRoute = Ember.Route.extend({
    model: function(){
        return this.store.filter('todo',function(todo){
            return !todo.get('isCompleted');
        });
    },
    renderTemplate: function(controller){
        this.render('todos/index', {controller: controller});
    },
});

App.TodosCompletedRoute = Ember.Route.extend({
    model: function(){
        return this.store.filter('todo',function(todo){
            return todo.get('isCompleted');
        });
    },
    renderTemplate: function(controller){
        this.render('todos/index', {controller: controller});
    },
});

/*==================================================*/

//Controllers
/*==================================================*/
App.TodosController = Ember.ArrayController.extend({
    remaining: function(){
        return this.filterBy('isCompleted',false).get('length');
    }.property('@each.isCompleted'),

    inflection: function(){
        var remaining = this.get('remaining');
        return remaining === 1 ? 'item' : 'items';
    }.property('remaining'),

    completedCount: function(){
        return this.filterBy('isCompleted',true).get('length');
    }.property('@each.isCompleted'),

    hasCompleted: function(){
        return this.get('completedCount') > 0;
    }.property('completedCount'),

    allAreDone: function(key,value){
        if (value === undefined) {
            return !!this.get('length') && this.everyProperty('isCompleted',true);
        }else{
            this.setEach('isCompleted',value);
            this.invoke('save')
            return value
        }
    }.property('@each.isCompleted'),

    actions: {
        createTodo: function(){
            //Get todo title set by "New Todo" input text field
            var title = this.get('newTitle');
            if (!title.trim()) { return; }

            //Create
            var todo = this.store.createRecord('todo',{
                data: {
                    title: title,
                    isCompleted: false
                }});
            // reset field input
            this.set('newTitle','');

            todo.save();
        },

        clearCompleted: function(){
            var completed = this.filterBy('isCompleted',true);
            completed.invoke('deleteRecord');
            completed.invoke('save');
        },

    }
})

App.TodoController = Ember.ObjectController.extend({
    isEditing: false,

    actions: {
        editTodo: function(){
            this.set('isEditing',true);
        },
        acceptChanges: function(title){
            this.set('isEditing',false);

            if(!title){
                this.send('removeTodo');
            }else{
                this.get('model').getOrSet('title',title);
            };
        },
        removeTodo: function(){
            var todo = this.get('model');
            todo.deleteRecord();
            todo.save();
        },
    },

});

/*==================================================*/

//Helpers
/*==================================================*/
App.EditTodoView = Ember.TextField.extend({
    didInsertElement: function(){
        this.$().focus();
    },
});

Ember.Handlebars.helper('edit-todo',App.EditTodoView);
/*==================================================*/
