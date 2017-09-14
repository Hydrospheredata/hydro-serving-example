def collectTestResults() {
    step([$class: 'JUnitResultArchiver', testResults: '**/target/surefire-reports/TEST-*.xml', allowEmptyResults: true])
}

def currentVersion() {
    return readFile("version").trim()
}

def changeVersion(version) {
    writeFile file: 'version', text: version
}

def calculateReleaseVersion(currentVersion) {
    def index=currentVersion.lastIndexOf("-SNAPSHOT")
    def releaseVersion
    if(index>-1){
        releaseVersion=currentVersion.substring(0, index)
    }else{
        releaseVersion=currentVersion
    }
    return releaseVersion
}

def calculateNextDevVersion(releaseVersion) {
    int index = releaseVersion.lastIndexOf('.')
    String minor = releaseVersion.substring(index + 1)
    int m = minor.toInteger() + 1
    return releaseVersion.substring(0, index + 1) + m + "-SNAPSHOT"
}

def checkoutSource(gitCredentialId, organization, repository) {
    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: gitCredentialId, usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
        git url: "https://github.com/${organization}/${repository}.git", branch: env.BRANCH_NAME, credentialsId: gitCredentialId
        sh """
            git config --global push.default simple
            git config --global user.name '${GIT_USERNAME}'
            git config --global user.email '${GIT_USERNAME}'
        """
    }
}

def pushSource(gitCredentialId, organization, repository, pushCommand) {
    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: gitCredentialId, usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD']]) {
        sh "git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/${organization}/${repository}.git ${pushCommand}"
    }
}

def isReleaseJob() {
    return "release".equalsIgnoreCase(env.BRANCH_NAME)
}

node("JenkinsOnDemand") {
    def repository = 'hydro-serving-runtime'
    def organization = 'Hydrospheredata'
    def gitCredentialId = 'HydrospheredataGithubAccessKey'


    stage('Checkout') {
        deleteDir()
        checkoutSource(gitCredentialId, organization, repository)
    }

    if (isReleaseJob()) {
        stage('Set release version') {
            def curVersion = currentVersion()
            def nextVersion=calculateReleaseVersion(curVersion)
            changeVersion(nextVersion)
        }
    }

    stage('Build') {
        def curVersion = currentVersion()
        sh "${env.WORKSPACE}/build.sh ${curVersion}"
    }

    stage('Test') {
        //TODO test???
    }
    if (isReleaseJob()) {
        //if (currentBuild.result == 'UNSTABLE') {
        //    currentBuild.result = 'FAILURE'
        //    error("Errors in tests")
        //}

        stage("Publish"){
            def curVersion = currentVersion()
            sh "git commit -m 'Releasing ${curVersion}' -- version"
            sh "git tag -a ${curVersion} -m 'Releasing ${curVersion}'"

            sh "git checkout master"

            def nextVersion=calculateNextDevVersion(curVersion)
            changeVersion(nextVersion)

            sh "git commit -m 'Development version increased: ${nextVersion}' -- version"

            pushSource(gitCredentialId, organization, repository, "")
            pushSource(gitCredentialId, organization, repository, "refs/tags/${curVersion}")
        }
    }
}