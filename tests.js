// ReshapeX Dashboard — Test Suite
// Run by opening test-runner.html in a browser, or by loading this file
// after data.js in a <script> tag. Results print to the console.

(function () {
  'use strict';

  // ── Test harness ────────────────────────────────────────────────

  const results = [];

  function assert(label, condition, detail) {
    const status = condition ? 'PASS' : 'FAIL';
    results.push({ status, label, detail });
    const style = condition
      ? 'color: #22c55e; font-weight: bold;'
      : 'color: #f87171; font-weight: bold;';
    const msg = detail ? `${status} — ${label} (${detail})` : `${status} — ${label}`;
    console.log('%c' + msg, style);
  }

  function section(title) {
    console.log('\n%c' + title, 'color: #818cf8; font-weight: bold; font-size: 13px;');
  }

  // ── Logic under test (mirrors reshapex.html) ────────────────────

  // Caps robot progress at 100 and transitions to 'deployed' if reached
  function applyProgressIncrement(robot, increment) {
    robot.progress = Math.min(100, robot.progress + increment);
    if (robot.progress >= 100) {
      robot.progress = 100;
      robot.status   = 'deployed';
    }
  }

  // Returns status counts for a given array of robots
  function computeCounts(robots) {
    const counts = { total: robots.length, deployed: 0, inprogress: 0, pending: 0 };
    robots.forEach(r => {
      if (counts[r.status] !== undefined) counts[r.status]++;
    });
    return counts;
  }

  // ── Sample data (used when ROBOTS_DATA is not available) ────────

  const SAMPLE_DATA = [
    { id: 'RBT-0041', type: 'Welding Unit',      client: 'Volcarex Auto',    status: 'deployed',   progress: 100, time: '07:14 AM', elapsed: '5h 22m' },
    { id: 'RBT-0078', type: 'Precision Drill',   client: 'Nexford Steel',    status: 'deployed',   progress: 100, time: '08:00 AM', elapsed: '4h 36m' },
    { id: 'RBT-0103', type: 'Assembly System',   client: 'Orbital Dynamics', status: 'deployed',   progress: 100, time: '06:45 AM', elapsed: '5h 51m' },
    { id: 'RBT-0055', type: 'Coating Robot',     client: 'Lumex Corp',       status: 'inprogress', progress: 63,  time: '10:20 AM', elapsed: '2h 16m' },
    { id: 'RBT-0089', type: 'Inspection Unit',   client: 'TerraFab Inc.',    status: 'inprogress', progress: 38,  time: '11:05 AM', elapsed: '1h 31m' },
    { id: 'RBT-0117', type: 'Laser Cutter',      client: 'Meridian Works',   status: 'inprogress', progress: 17,  time: '11:48 AM', elapsed: '0h 48m' },
    { id: 'RBT-0132', type: 'Heavy Lift System', client: 'Vantage Metals',   status: 'pending',    progress: 0,   time: '—',        elapsed: 'Not started' },
    { id: 'RBT-0150', type: 'Sorting Unit',      client: 'CorePlex Mfg.',    status: 'pending',    progress: 0,   time: '—',        elapsed: 'Not started' },
  ];

  // Prefer the real data file if already loaded on the page
  const sourceData = (typeof ROBOTS_DATA !== 'undefined') ? ROBOTS_DATA : SAMPLE_DATA;

  // Deep-copy so tests never mutate shared state
  function clone(data) {
    return JSON.parse(JSON.stringify(data));
  }

  // ── Test 1 · Unit: progress is always capped at 100% ────────────

  section('1 · Unit — Progress cap');

  (function testProgressCap() {
    const robot = { id: 'RBT-TEST', status: 'inprogress', progress: 90 };

    // Exact cap: 90 + 10 = 100
    applyProgressIncrement(robot, 10);
    assert('progress reaches exactly 100 when increment lands on it',
      robot.progress === 100 && robot.status === 'deployed');

    // Overflow: start at 85, add 50 — must not exceed 100
    const r2 = { id: 'RBT-TEST2', status: 'inprogress', progress: 85 };
    applyProgressIncrement(r2, 50);
    assert('progress does not exceed 100 on large increment',
      r2.progress === 100,
      `got ${r2.progress}`);

    // Transition: hitting 100 flips status to deployed
    const r3 = { id: 'RBT-TEST3', status: 'inprogress', progress: 95 };
    applyProgressIncrement(r3, 20);
    assert('status transitions to deployed when progress reaches 100',
      r3.status === 'deployed');

    // In-flight: increment that stays below 100 keeps status as inprogress
    const r4 = { id: 'RBT-TEST4', status: 'inprogress', progress: 40 };
    applyProgressIncrement(r4, 15);
    assert('status stays inprogress when progress is below 100',
      r4.status === 'inprogress' && r4.progress === 55,
      `progress=${r4.progress}, status=${r4.status}`);
  })();

  // ── Test 2 · Integration: all robots have required fields ────────

  section('2 · Integration — Required fields');

  (function testRequiredFields() {
    const REQUIRED = ['id', 'status', 'progress', 'time'];
    const VALID_STATUSES = ['deployed', 'inprogress', 'pending'];
    const data = clone(sourceData);

    let allHaveFields = true;
    let allValidStatus = true;
    let allValidProgress = true;
    let allValidTypes = true;
    const missing = [];

    data.forEach(robot => {
      REQUIRED.forEach(field => {
        if (!(field in robot) || robot[field] === null || robot[field] === undefined) {
          allHaveFields = false;
          missing.push(`${robot.id || '?'}.${field}`);
        }
      });

      if (!VALID_STATUSES.includes(robot.status)) {
        allValidStatus = false;
      }

      if (typeof robot.progress !== 'number' || robot.progress < 0 || robot.progress > 100) {
        allValidProgress = false;
      }

      if (typeof robot.id !== 'string' || robot.id.trim() === '') {
        allValidTypes = false;
      }
    });

    assert('every robot has all required fields (id, status, progress, time)',
      allHaveFields,
      missing.length ? `missing: ${missing.join(', ')}` : `checked ${data.length} robots`);

    assert('every robot has a valid status value',
      allValidStatus,
      `valid values: ${VALID_STATUSES.join(', ')}`);

    assert('every robot progress is a number between 0 and 100',
      allValidProgress);

    assert('every robot id is a non-empty string',
      allValidTypes);

    assert(`dataset contains exactly 8 robots`,
      data.length === 8,
      `found ${data.length}`);
  })();

  // ── Test 3 · Regression: counters update when status changes ─────

  section('3 · Regression — Status counter updates');

  (function testCounterUpdates() {
    const data = clone(sourceData);

    const before = computeCounts(data);

    // Simulate one pending robot transitioning to deployed
    const target = data.find(r => r.status === 'pending');
    if (!target) {
      assert('found a pending robot to transition', false, 'no pending robots in dataset');
      return;
    }
    target.status   = 'deployed';
    target.progress = 100;

    const after = computeCounts(data);

    assert('total count is unchanged after status transition',
      after.total === before.total,
      `before=${before.total}, after=${after.total}`);

    assert('deployed count increases by 1',
      after.deployed === before.deployed + 1,
      `before=${before.deployed}, after=${after.deployed}`);

    assert('pending count decreases by 1',
      after.pending === before.pending - 1,
      `before=${before.pending}, after=${after.pending}`);

    assert('inprogress count is unchanged',
      after.inprogress === before.inprogress,
      `before=${before.inprogress}, after=${after.inprogress}`);

    // Verify the percentage calculation stays in valid range
    const pct = Math.round((after.deployed / after.total) * 100);
    assert('deployed percentage is between 0 and 100',
      pct >= 0 && pct <= 100,
      `${pct}%`);
  })();

  // ── Summary ─────────────────────────────────────────────────────

  const passed = results.filter(r => r.status === 'PASS').length;
  const failed = results.filter(r => r.status === 'FAIL').length;

  console.log(
    `\n%c${'─'.repeat(48)}\n  Results: ${passed} passed, ${failed} failed (${results.length} total)\n${'─'.repeat(48)}`,
    failed > 0
      ? 'color: #f87171; font-weight: bold;'
      : 'color: #22c55e; font-weight: bold;'
  );

  // Expose results for programmatic access if needed
  window.testResults = results;
})();
