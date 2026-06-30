module.exports = {
  id: 'atu-noop',
  async callApi(prompt, context) {
    return {
      output: JSON.stringify({
        ok: true,
        episode_id: context.vars.episode_id,
        replay_class: context.vars.replay_class
      })
    };
  }
};
