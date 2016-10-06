node {
	stage 'Checkout'
	checkout scm

	stage 'Install requirements'
    // bat 'conda install -c Quantopian zipline'
    bat 'pip install -r requirements.txt'

	stage 'Test'
	bat 'nosetests -w tests --with-coverage --cover-package=rikedom'

	stage 'Archive'
	archive 'nosetests.xml'
}
