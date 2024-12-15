<script lang="ts">
  import type { IUser } from "../utils/types";

  interface Props {
    user: IUser;
  }

  let { user }: Props = $props();

  function handleOpenUserForm(e: MouseEvent) {
    e.preventDefault();
    const form = document.getElementById("user");
    form.style.display = "block";
  }

  function handleUpdate(e: Event) {
    e.preventDefault();
    console.log(user);
  }

  function handleCancel() {
    const form = document.getElementById("user");
    form.style.display = "none";
  }
</script>

<div>
  <small>
    <strong>usuario:</strong>
    <a href="#user" onclick={handleOpenUserForm}>
      {user.name}
    </a>
  </small>

  <div id="user">
    <form onsubmit={handleUpdate}>
      <div class="form-control">
        <label for="name">Nombre:</label>
        <input type="text" id="name" name="name" bind:value={user.name} />
      </div>
      <div class="form-control">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" bind:value={user.email} />
      </div>
      <div class="form-actions">
        <button type="button" onclick={handleCancel}>Cancelar</button>
        <button type="submit" class="secondary">Guardar</button>
      </div>
    </form>
  </div>
</div>

<style>
  #user {
    display: none;
    position: absolute;
    width: 90%;
    left: 50%;
    transform: translateX(-50%);
    top: 30%;
    z-index: 9999;
  }

  form {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;

    .form-control {
      display: flex;
      align-items: center;
      gap: 8px;

      label {
        min-width: 70px;
        text-align: right;
      }

      input {
        width: calc(100% - 70px);
      }
    }

    .form-actions {
      margin-top: 12px;
      display: flex;
      justify-content: space-between;
    }
  }
</style>
