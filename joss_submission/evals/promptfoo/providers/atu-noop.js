module.exports = class AtuNoopProvider {
  constructor(options = {}) {
    this.providerId = options.id || 'atu-noop';
  }

  id() {
    return this.providerId;
  }

  async callApi(prompt, context) {
    return {
      output: JSON.stringify({
        ok: true,
        episode_id: context.vars.episode_id,
        replay_class: context.vars.replay_class,
        prompt
      })
    };
  }
};
