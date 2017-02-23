(function () {
    'use strict';

    angular
        .module('app.todo')
        .controller('TaskDialogController', TaskDialogController);

    /** @ngInject */
    function TaskDialogController($mdDialog, Task, Tasks, event, $http) {
        var vm = this;

        // Data
        vm.title = 'Edit Task';
        vm.task = angular.copy(Task);
        vm.tasks = Tasks;
        vm.newTask = false;

        if (!vm.task) {
            vm.task = {
                'id': 1,
                'title': '',
                'notes': '',
                'start_date': new Date(),
                'startDateTimeStamp': new Date().getTime(),
                'due_date': '',
                'dueDateTimeStamp': '',
                'completed': false,
                'starred': false,
                'important': false,
                'deleted': false,
                'tags': []
            };
            vm.title = 'New Task';
            vm.newTask = true;
            vm.task.tags = [];
        }

        // Methods
        vm.addNewTask = addNewTask;
        vm.saveTask = saveTask;
        vm.deleteTask = deleteTask;
        vm.newTag = newTag;
        vm.closeDialog = closeDialog;

        //////////


        /**
         * Add new task
         * "2017-02-23T20:58:17.283Z"
         */
        function addNewTask() {
            vm.tasks.unshift(vm.task);
            console.log('TASK ADDED!!!');
            console.log(vm.task);
            console.log(vm.task.dueDateTimeStamp);
            console.log(vm.task.due_date);

            var csrf = document.getElementsByName("csrfmiddlewaretoken");
            $http({
                method: 'POST',
                url: '/todo/todolist/?format=json',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf[0].value
                },
                data: vm.task
            }).then(function successCallback(response) {
                console.log('SUCCESS WITH PUT METHOD');
            }, function errorCallback(response) {
                console.log('ERROR WITH PUT METHOD');
            });
            closeDialog();
        }

        /**
         * Save task
         */
        function saveTask() {
            // Dummy save action
            for (var i = 0; i < vm.tasks.length; i++) {
                if (vm.tasks[i].id === vm.task.id) {
                    vm.tasks[i] = angular.copy(vm.task);
                    console.log('TASK SAVED!!');

                    var csrf = document.getElementsByName("csrfmiddlewaretoken");

                    $http({
                        method: 'PUT',
                        url: '/todo/' + vm.tasks[i].id + '/?format=json',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrf[0].value
                        },
                        data: vm.tasks[i]
                    }).then(function successCallback(response) {
                        console.log('SUCCESS WITH PUT METHOD');
                    }, function errorCallback(response) {
                        console.log('ERROR WITH PUT METHOD');
                    });
                    break;
                }
            }

            closeDialog();
        }


        /**
         * Delete task
         */
        function deleteTask() {
            var confirm = $mdDialog.confirm()
                .title('Are you sure?')
                .content('The Task will be deleted.')
                .ariaLabel('Delete Task')
                .ok('Delete')
                .cancel('Cancel')
                .targetEvent(event);

            $mdDialog.show(confirm).then(function () {
                // Dummy delete action
                for (var i = 0; i < vm.tasks.length; i++) {
                    if (vm.tasks[i].id === vm.task.id) {
                        vm.tasks[i].deleted = true;
                        break;
                    }
                }
            }, function () {
                // Cancel Action
            });
        }


        /**
         * New tag
         *
         * @param chip
         * @returns {#label: *, color: string#}
         */
        function newTag(chip) {
            var tagColors = ['#388E3C', '#F44336', '#FF9800', '#0091EA', '#9C27B0'];

            console.log('NEW TAG ADDED!!');
            var newTag = {
                name: chip,
                label: chip,
                color: tagColors[Math.floor(Math.random() * (tagColors.length))]
            };

            console.log(newTag.name);
            console.log(newTag.label);
            console.log(newTag.color);

            return newTag;
        }

        /**
         * Close dialog
         */
        function closeDialog() {
            $mdDialog.hide();
        }
    }
})();