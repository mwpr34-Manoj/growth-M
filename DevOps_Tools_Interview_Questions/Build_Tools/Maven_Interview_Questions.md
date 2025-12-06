# Maven Interview Questions & Answers

## 🚀 **Maven Fundamentals**

### 1. What is Maven and what are its key features?

**Answer:**
Maven is a build automation and project management tool primarily used for Java projects. It uses a Project Object Model (POM) to manage project dependencies, build lifecycle, and plugins.

**Key Features:**
- **Dependency Management**: Automatically downloads and manages project dependencies
- **Build Lifecycle**: Standardized build process (compile, test, package, install, deploy)
- **Project Object Model (POM)**: XML-based project configuration
- **Plugins**: Extensible plugin architecture
- **Convention over Configuration**: Standard directory structure
- **Repository Management**: Local and remote artifact repositories
- **Multi-module Projects**: Support for building multiple projects together

**Advantages:**
- Standardized project structure
- Automatic dependency resolution
- Consistent build process
- Large plugin ecosystem
- Integration with IDEs

---

### 2. What is the Maven project structure?

**Answer:**
Maven follows a convention-based directory structure.

**Standard Directory Layout:**
```
project-root/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/          # Main Java source code
│   │   ├── resources/     # Main resources (config files)
│   │   └── webapp/        # Web application files (for WAR)
│   └── test/
│       ├── java/          # Test Java source code
│       └── resources/     # Test resources
└── target/                # Build output (generated)
```

**Key Directories:**
- `src/main/java`: Application source code
- `src/main/resources`: Application resources
- `src/test/java`: Test source code
- `src/test/resources`: Test resources
- `target`: Compiled classes and artifacts

---

### 3. What is a POM file and what are its key elements?

**Answer:**
POM (Project Object Model) is an XML file that contains project configuration.

**Basic POM Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <!-- Project Coordinates -->
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <!-- Project Information -->
    <name>My Application</name>
    <description>Application description</description>
    
    <!-- Properties -->
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    
    <!-- Dependencies -->
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <!-- Build Configuration -->
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
                <configuration>
                    <source>11</source>
                    <target>11</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

**Key Elements:**
- `groupId`: Organization/group identifier
- `artifactId`: Project identifier
- `version`: Project version
- `packaging`: Artifact type (jar, war, pom)
- `dependencies`: Project dependencies
- `build`: Build configuration and plugins

---

### 4. What are Maven coordinates (GAV)?

**Answer:**
Maven coordinates uniquely identify a project using three values: GroupId, ArtifactId, and Version (GAV).

**GAV Components:**
- **GroupId**: Organization or group (e.g., `com.example`, `org.apache`)
- **ArtifactId**: Project name (e.g., `my-app`, `commons-lang`)
- **Version**: Project version (e.g., `1.0.0`, `2.3-SNAPSHOT`)

**Example:**
```xml
<groupId>com.example</groupId>
<artifactId>my-app</artifactId>
<version>1.0.0</version>
```

**Resulting Artifact:**
- File: `my-app-1.0.0.jar`
- Repository path: `com/example/my-app/1.0.0/my-app-1.0.0.jar`

---

### 5. What is the Maven build lifecycle?

**Answer:**
Maven has three built-in lifecycles, each with multiple phases.

**Default Lifecycle Phases:**
1. `validate`: Validate project is correct
2. `compile`: Compile source code
3. `test`: Run unit tests
4. `package`: Package compiled code (JAR, WAR, etc.)
5. `verify`: Run integration tests
6. `install`: Install to local repository
7. `deploy`: Deploy to remote repository

**Clean Lifecycle:**
- `clean`: Remove target directory

**Site Lifecycle:**
- `site`: Generate project documentation

**Running Phases:**
```bash
# Run specific phase (runs all previous phases)
mvn compile
mvn test
mvn package
mvn install

# Run multiple phases
mvn clean install
mvn clean package
```

---

### 6. How do you manage dependencies in Maven?

**Answer:**
Dependencies are declared in the `<dependencies>` section of POM.

**Adding Dependencies:**
```xml
<dependencies>
    <!-- Compile scope (default) -->
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>5.3.21</version>
    </dependency>
    
    <!-- Test scope -->
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.13.2</version>
        <scope>test</scope>
    </dependency>
    
    <!-- Provided scope -->
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>servlet-api</artifactId>
        <version>2.5</version>
        <scope>provided</scope>
    </dependency>
</dependencies>
```

**Dependency Scopes:**
- `compile`: Default, available in all classpaths
- `test`: Only for test compilation and execution
- `provided`: Provided by JDK or container
- `runtime`: Required at runtime, not compile time
- `system`: Similar to provided, but must provide path
- `import`: Only for dependency management in POM type

**Excluding Dependencies:**
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>my-lib</artifactId>
    <version>1.0.0</version>
    <exclusions>
        <exclusion>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

---

### 7. What are Maven repositories and how do they work?

**Answer:**
Repositories store artifacts (JARs, WARs, etc.) and metadata.

**Repository Types:**
1. **Local Repository**: `~/.m2/repository` (default)
2. **Central Repository**: Maven Central (public)
3. **Remote Repository**: Custom repositories (Nexus, Artifactory)

**Repository Configuration:**
```xml
<repositories>
    <repository>
        <id>central</id>
        <name>Maven Central</name>
        <url>https://repo1.maven.org/maven2</url>
    </repository>
    <repository>
        <id>custom-repo</id>
        <url>https://repo.example.com/maven</url>
    </repository>
</repositories>
```

**Settings.xml Configuration:**
```xml
<!-- ~/.m2/settings.xml -->
<settings>
    <localRepository>/path/to/local/repo</localRepository>
    <mirrors>
        <mirror>
            <id>nexus</id>
            <mirrorOf>*</mirrorOf>
            <url>http://nexus.example.com/repository/maven-public/</url>
        </mirror>
    </mirrors>
</settings>
```

---

### 8. How do you use Maven plugins?

**Answer:**
Plugins extend Maven's functionality.

**Common Plugins:**
```xml
<build>
    <plugins>
        <!-- Compiler Plugin -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.8.1</version>
            <configuration>
                <source>11</source>
                <target>11</target>
            </configuration>
        </plugin>
        
        <!-- Surefire Plugin (Tests) -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.22.2</version>
        </plugin>
        
        <!-- JAR Plugin -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-jar-plugin</artifactId>
            <version>3.2.0</version>
            <configuration>
                <archive>
                    <manifest>
                        <mainClass>com.example.Main</mainClass>
                    </manifest>
                </archive>
            </configuration>
        </plugin>
    </plugins>
</build>
```

**Executing Plugin Goals:**
```bash
# Run specific plugin goal
mvn compiler:compile
mvn surefire:test
mvn jar:jar

# Run with parameters
mvn compiler:compile -Dmaven.compiler.source=11
```

---

### 9. How do you create multi-module projects in Maven?

**Answer:**
Multi-module projects allow building multiple projects together.

**Parent POM:**
```xml
<!-- parent/pom.xml -->
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>parent-project</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>
    
    <modules>
        <module>module1</module>
        <module>module2</module>
        <module>module3</module>
    </modules>
    
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
    </properties>
</project>
```

**Child Module POM:**
```xml
<!-- parent/module1/pom.xml -->
<project>
    <parent>
        <groupId>com.example</groupId>
        <artifactId>parent-project</artifactId>
        <version>1.0.0</version>
    </parent>
    
    <artifactId>module1</artifactId>
    <packaging>jar</packaging>
    
    <dependencies>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>module2</artifactId>
            <version>${project.version}</version>
        </dependency>
    </dependencies>
</project>
```

**Building:**
```bash
# Build all modules
mvn clean install

# Build specific module
mvn clean install -pl module1
```

---

### 10. How do you handle Maven profiles?

**Answer:**
Profiles allow different configurations for different environments.

**Profile Definition:**
```xml
<profiles>
    <profile>
        <id>dev</id>
        <properties>
            <env>development</env>
        </properties>
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
    </profile>
    
    <profile>
        <id>prod</id>
        <properties>
            <env>production</env>
        </properties>
        <build>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <configuration>
                        <source>11</source>
                        <target>11</target>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    </profile>
</profiles>
```

**Activating Profiles:**
```bash
# Activate specific profile
mvn clean install -Pprod

# Activate multiple profiles
mvn clean install -Pdev,test

# Activate via property
mvn clean install -Denv=prod
```

---

### 11. How do you manage Maven versions and SNAPSHOT?

**Answer:**
**Version Types:**
- **Release**: Stable version (e.g., `1.0.0`)
- **SNAPSHOT**: Development version (e.g., `1.0.0-SNAPSHOT`)

**SNAPSHOT Versions:**
```xml
<version>1.0.0-SNAPSHOT</version>
```
- Maven checks for updates on each build
- Used for development
- Can be overwritten

**Release Versions:**
```xml
<version>1.0.0</version>
```
- Immutable once deployed
- Used for production

**Version Management:**
```bash
# Set version
mvn versions:set -DnewVersion=2.0.0

# Update parent version
mvn versions:update-parent

# Update dependencies
mvn versions:use-latest-versions
```

---

### 12. How do you troubleshoot Maven build issues?

**Answer:**
**Common Issues and Solutions:**

1. **Dependency Not Found:**
```bash
# Update dependencies
mvn dependency:resolve

# Check dependency tree
mvn dependency:tree

# Download sources
mvn dependency:sources
```

2. **Build Failures:**
```bash
# Clean and rebuild
mvn clean install

# Skip tests
mvn clean install -DskipTests

# Run with debug
mvn clean install -X

# Check effective POM
mvn help:effective-pom
```

3. **Repository Issues:**
```bash
# Update repository index
mvn dependency:purge-local-repository

# Clear local repository cache
rm -rf ~/.m2/repository
```

---

## 📝 **Best Practices**

1. **Use consistent versioning**: Follow semantic versioning
2. **Manage dependencies**: Keep dependencies up to date
3. **Use properties**: Centralize version numbers
4. **Profile management**: Use profiles for different environments
5. **Plugin management**: Centralize plugin versions in parent POM
6. **Documentation**: Keep README updated
7. **Testing**: Run tests before deploying
8. **Security**: Scan dependencies for vulnerabilities
9. **CI/CD**: Integrate Maven with CI/CD pipelines
10. **Repository**: Use private repository for internal artifacts

---

**Good luck with your Maven interview preparation!**
