<template>
  <div class="bio">
    <strong>{{ this.meta.FullName }}</strong>
    <br/>
    <div class="divider"></div>
    <small>
      {{ this.meta.TeamLong }}, {{ this.meta.Position }}

      <div class="meta">
        <div>
          <strong>Born:</strong> {{ this.meta.Birthday }}
          ({{ calculateYearsFromToday(this.meta.Birthday) }})
        </div>
        <div>
          <strong>MLB Debut:</strong> {{ this.meta.Debut }}
          ({{ calculateYearsFromToday(this.meta.Debut) }})
        </div>
        <div>
          <strong>Bats:</strong> {{ formatHandedness(this.meta.Bats) }}
          |
          <strong>Throws:</strong> {{ formatHandedness(this.meta.Throws) }}
        </div>
      </div>
    </small>
  </div>
</template>

<script>
export default {
  name: 'Bio',

  props: ['meta'],

  methods: {
    calculateYearsFromToday(date) {
      date = new Date(date);
      const age_diff_ms = Date.now() - date.getTime();
      const age_diff = new Date(age_diff_ms); // miliseconds from epoch
      return Math.abs(age_diff.getUTCFullYear() - 1970);
    },
    formatHandedness(value) {
      value = value.toLowerCase();
      if (value == 'l') {
        value = 'Left';
      } else if (value == 'r') {
        value = 'Right';
      } else if (value == 's') {
        value = 'Switch';
      }
      return value;
    }
  }
};
</script>

<style>
  .bio {
    width: 100%;
  }
  .divider {
    border: 1px dotted #ddd;
  }
  .meta {
    font-size: 90%;
    margin-top: 15px;
    line-height: 1.5rem;
  }
</style>