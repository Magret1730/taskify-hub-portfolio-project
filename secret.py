import os

# Generate a secret key
secret_key = os.urandom(24)

print(secret_key.hex())

# order = db.Column(db.Integer, nullable=False)
# self.order = Todo.query.filter_by(reg_id=reg_id).count() + 1

# {% for todo in todo_list %}
#             <div class="card-body shadow">
#                 <h5 class="mb-0">{{ todo.title }}</h5>
#                 <p class="container-fluid">{{ todo.description }}</p>
#                 <p class="container-fluid mb-0"><b>Due Date:</b> {{ todo.due_date.strftime('%Y-%m-%d') if todo.due_date else 'Not specified' }}</p>
#                 <div class="container-fluid">
#                     {% if todo.complete %}
#                     <span class="badge bg-success">Completed</span>
#                     {% else %}
#                     <span class="badge bg-secondary">Uncompleted</span>
#                     {% endif %}
#                     <a class="btn btn-sm btn-info" href="/update/{{ todo.id }}">Mark Completed</a>

#                     <button type="button" class="btn btn-sm btn-secondary custom-bg" data-bs-toggle="modal" data-bs-target="#editModal{{ todo.id }}">
#                         Edit
#                     </button>
                    
#                     Modal
#                     <div class="modal fade" id="editModal{{ todo.id }}" tabindex="-1" aria-labelledby="editModal{{ todo.id }}Label"
#                         aria-hidden="true">
#                         <div class="modal-dialog">
#                             <div class="modal-content bg custom-textt">
#                                 <div class="modal-header">
#                                     <h5 class="modal-title" id="editModal{{ todo.id }}Label"><b>EDIT TASK</b></h5>
#                                     <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
#                                 </div>
#                                 <div class="modal-body">
#                                     <form id="editForm{{ todo.id }}" method="post" action="/edit/{{ todo.id }}">
#                                         <input type="hidden" name="_method" value="put">
#                                         <div class="mb-3">
#                                             <label for="titleInput{{ todo.id }}" class="form-label">New Title</label>
#                                             <input type="text" class="form-control" id="titleInput{{ todo.id }}" name="title" placeholder="New Title"
#                                                 value="{{ todo.title }}">
#                                         </div>
#                                         <div class="mb-3">
#                                             <label for="descriptionInput{{ todo.id }}" class="form-label">New Description</label>
#                                             <textarea class="form-control" id="descriptionInput{{ todo.id }}" name="description"
#                                                 placeholder="New Description">{{ todo.description }}</textarea>
#                                         </div>
#                                         <div class="mb-3">
#                                             <label for="dueDateInput{{ todo.id }}" class="form-label">Due Date</label>
#                                             <input type="date" class="form-control" id="dueDateInput{{ todo.id }}" name="due_date"
#                                                 value="{{ todo.due_date.strftime('%Y-%m-%d') if todo.due_date else '' }}">
#                                         </div>
#                                         <button type="submit" class="btn btn-secondary custom-bg">Save</button>
#                                     </form>
#                                 </div>
#                             </div>
#                         </div>
#                     </div>
#                     <a class="btn btn-sm btn-danger" href="/delete/{{ todo.id }}">Delete</a>
#                 </div>
#             </div>
#             {% endfor %}