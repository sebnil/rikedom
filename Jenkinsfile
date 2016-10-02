node {
	stage('Checkout') {
		checkout scm
	}

	stage('Test') {
		bat 'nosetests -w tests --with-coverage --cover-package=rikedom'
    }

	stage('Archive') {
		archive '.coverage'
		archive '.nosetests.xml'
	}
}