node {
	stage('Checkout')
	{
		checkout scm
	}

	stage('Create Virtual Environment')
	{
		try {		
			bat 'conda create --name rikedom python=3.5 --yes'
		}
		catch (Exception ex)
		{
			
		}
		bat 'activate rikedom && conda update python'
	}

	stage('Install requirements')
	{
	    bat 'activate python_uptimer && conda install -c Quantopian zipline --yes'
	    bat 'activate python_uptimer && pip install -r requirements.txt'
	}

	stage('Test')
	{
		bat 'activate python_uptimer && nosetests -w tests --with-xunit --with-coverage --cover-package=rikedom --verbosity=2'
	}

	/*stage('Remove Virtual Environment')
	{
		bat 'conda remove --name rikedom --all --yes'
	}*/

	stage('Archive')
	{
		archive 'nosetests.xml'
	}
	
	stage('Publish')
	{
		step([$class: 'JUnitResultArchiver', testResults: 'nosetests.xml'])
	}
}
