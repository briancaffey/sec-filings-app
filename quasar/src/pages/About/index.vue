<template>
  <q-page padding>
    <q-card>
      <q-card-section>
        <div class="text-h6">About this project</div>
        <div>
          This is an open-source project that pulls public filing data from
          sec.gov and builds makes that data accessible through a public API.
          Currently this project is focused on 13F filings. Other filing types
          may be added in the future or upon request.
        </div>
      </q-card-section>
      <q-card-section>
        <div class="text-h6">Technologies</div>
        This project is built with the following technologies, languages and
        Frameworks:
        <ul>
          <li>Python, Django and PostgreSQL on the backend</li>
          <li>Javascript, Vue.js and Quasar Framework for the frontend</li>
          <li>Running on DigitalOcean using docker and docker swarm</li>
          <li>Deployed with GitLab</li>
          <li>Apex Charts charting library</li>
        </ul>
      </q-card-section>
      <q-card-section>
        <div class="text-h6">Data access</div>
        <div>
          To access the Public API, please sign up for an account with LinkedIn
          and request an account on <a href="/account">your account page</a>.
        </div>
      </q-card-section>
      <q-card-section>
        <div class="text-h6">Similar Projects</div>
        Here are some similar projects:
        <ul>
          <li><a href="https://formthirteen.com">formthirteen.com</a></li>
          <li><a href="https://whalewisdom.com/">whalewisdom.com</a></li>
          <li><a href="http://sec-api.io/">sec-api.io</a></li>
        </ul>
      </q-card-section>
      <q-card-section>
        <div class="text-h6">Source Code</div>
        <div>
          For more information you can view the source code here. You will need
          to be logged in to a GitLab account to view this code on GitLab.
        </div>
        <div>
          Code on GitHub is a mirror of the code on GitLab. All issues will be
          tracked on the GitLab repository. Deployment and continuous
          integration pipelines run through GitLab CI.
        </div>
        <div>
          <br />
          <q-card-section>
            <q-btn
              type="a"
              href="https://gitlab.com/briancaffey/sec-filings-app"
            >
              Soure code on gitlab.com
            </q-btn>
          </q-card-section>
          <q-card-section>
            <q-btn
              type="a"
              href="https://github.com/briancaffey/sec-filings-app"
            >
              Soure code on github.com
            </q-btn>
          </q-card-section>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
export default {};
</script>

<style scoped></style>
