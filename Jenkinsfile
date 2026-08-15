pipeline {
  agent { label 'python-3.11-playwright' }
  parameters { choice(name: 'SUITE', choices: ['smoke', 'regression', 'admin'], description: 'UI suite') }
  stages {
    stage('Bootstrap') { steps { dir('ui-automation') { powershell '.\\scripts\\bootstrap.ps1' } } }
    stage('Unit') { steps { dir('ui-automation') { powershell '.\\.venv\\Scripts\\python.exe -m unittest discover -s tests\\unit' } } }
    stage('UI') { steps { dir('ui-automation') { powershell ".\\scripts\\run.ps1 -Suite ${params.SUITE}" } } }
  }
  post {
    always { archiveArtifacts artifacts: 'ui-automation/reports/**/*', allowEmptyArchive: true }
    always { junit testResults: 'ui-automation/reports/ui-junit.xml', allowEmptyResults: true }
  }
}
