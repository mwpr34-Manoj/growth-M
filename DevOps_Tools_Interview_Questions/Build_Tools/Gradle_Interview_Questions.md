# Gradle Interview Questions & Answers

## 🚀 **Gradle Fundamentals**

### 1. What is Gradle and how does it differ from Maven?

**Answer:**
Gradle is a build automation tool that combines the best features of Ant and Maven. It uses a Groovy or Kotlin DSL for build scripts.

**Key Differences from Maven:**

| Feature | Gradle | Maven |
|---------|--------|-------|
| **Build Script** | Groovy/Kotlin DSL | XML (POM) |
| **Flexibility** | Highly flexible | Convention-based |
| **Performance** | Faster (incremental builds) | Slower |
| **Dependency Management** | Advanced (transitive) | Basic |
| **Multi-project** | Better support | Good support |
| **Learning Curve** | Steeper | Easier |

**Advantages:**
- More flexible than Maven
- Faster builds (incremental compilation)
- Better dependency management
- Supports multiple languages (Java, Kotlin, Groovy, Scala)
- Powerful plugin system

---

### 2. What is the Gradle project structure?

**Answer:**
Gradle follows a convention-based structure similar to Maven.

**Standard Directory Layout:**
```
project-root/
├── build.gradle          # Build script (Groovy)
├── build.gradle.kts      # Build script (Kotlin)
├── settings.gradle       # Project settings
├── gradle.properties     # Gradle properties
├── gradlew               # Gradle wrapper (Unix)
├── gradlew.bat           # Gradle wrapper (Windows)
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── src/
│   ├── main/
│   │   ├── java/         # Main Java source
│   │   ├── resources/    # Main resources
│   │   └── webapp/       # Web application (WAR)
│   └── test/
│       ├── java/         # Test Java source
│       └── resources/   # Test resources
└── build/                # Build output
```

---

### 3. What is a build.gradle file and what are its key elements?

**Answer:**
`build.gradle` is the main build script using Groovy DSL.

**Basic build.gradle:**
```groovy
// Plugins
plugins {
    id 'java'
    id 'application'
}

// Project information
group = 'com.example'
version = '1.0.0'

// Java version
java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

// Repositories
repositories {
    mavenCentral()
    maven {
        url 'https://repo.example.com/maven'
    }
}

// Dependencies
dependencies {
    // Implementation dependencies
    implementation 'org.springframework:spring-core:5.3.21'
    
    // Test dependencies
    testImplementation 'junit:junit:4.13.2'
    
    // Runtime dependencies
    runtimeOnly 'mysql:mysql-connector-java:8.0.33'
}

// Application configuration
application {
    mainClass = 'com.example.Main'
}

// Custom tasks
task hello {
    doLast {
        println 'Hello, Gradle!'
    }
}
```

**Kotlin DSL (build.gradle.kts):**
```kotlin
plugins {
    java
    application
}

group = "com.example"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework:spring-core:5.3.21")
    testImplementation("junit:junit:4.13.2")
}

application {
    mainClass.set("com.example.Main")
}
```

---

### 4. How do you manage dependencies in Gradle?

**Answer:**
Dependencies are declared in the `dependencies` block.

**Dependency Configurations:**
```groovy
dependencies {
    // Compile time and runtime
    implementation 'com.example:library:1.0.0'
    
    // Compile time only
    compileOnly 'javax.servlet:servlet-api:2.5'
    
    // Runtime only
    runtimeOnly 'mysql:mysql-connector-java:8.0.33'
    
    // Test compile and runtime
    testImplementation 'junit:junit:4.13.2'
    
    // Test runtime only
    testRuntimeOnly 'org.hamcrest:hamcrest:2.2'
    
    // Annotation processor
    annotationProcessor 'com.google.auto.value:auto-value:1.9'
}
```

**Dependency Types:**
- `implementation`: Main dependencies
- `api`: Dependencies exposed to consumers
- `compileOnly`: Compile-time only
- `runtimeOnly`: Runtime only
- `testImplementation`: Test dependencies
- `testCompileOnly`: Test compile-time only
- `testRuntimeOnly`: Test runtime only

**Excluding Dependencies:**
```groovy
dependencies {
    implementation('com.example:library:1.0.0') {
        exclude group: 'org.slf4j', module: 'slf4j-api'
    }
}
```

**Dynamic Versions:**
```groovy
dependencies {
    implementation 'com.example:library:1.+'
    implementation 'com.example:library:latest.release'
}
```

---

### 5. What are Gradle tasks and how do you create custom tasks?

**Answer:**
Tasks are units of work in Gradle.

**Built-in Tasks:**
```bash
# List all tasks
./gradlew tasks

# Common tasks
./gradlew build
./gradlew clean
./gradlew test
./gradlew jar
./gradlew run
```

**Creating Custom Tasks:**
```groovy
// Simple task
task hello {
    doLast {
        println 'Hello, Gradle!'
    }
}

// Task with configuration
task copyFiles(type: Copy) {
    from 'src/main/resources'
    into 'build/output'
    include '*.properties'
}

// Task with dependencies
task buildAll {
    dependsOn 'compile', 'test', 'jar'
    doLast {
        println 'Build completed'
    }
}

// Task with properties
task deploy {
    description = 'Deploy application'
    group = 'deployment'
    
    doLast {
        println "Deploying version ${project.version}"
    }
}
```

**Task Execution:**
```bash
# Run specific task
./gradlew hello

# Run multiple tasks
./gradlew clean build

# Skip task
./gradlew build -x test
```

---

### 6. How do you use Gradle plugins?

**Answer:**
Plugins extend Gradle functionality.

**Applying Plugins:**
```groovy
// Using plugins block (recommended)
plugins {
    id 'java'
    id 'application'
    id 'org.springframework.boot' version '2.7.0'
}

// Using apply plugin (legacy)
apply plugin: 'java'
apply plugin: 'application'
```

**Common Plugins:**
```groovy
plugins {
    id 'java'                    // Java support
    id 'application'             // Application plugin
    id 'war'                     // WAR packaging
    id 'org.springframework.boot' version '2.7.0'
    id 'io.spring.dependency-management' version '1.0.11.RELEASE'
}
```

**Plugin Configuration:**
```groovy
application {
    mainClass = 'com.example.Main'
}

jar {
    archiveBaseName = 'myapp'
    archiveVersion = '1.0.0'
    manifest {
        attributes 'Main-Class': 'com.example.Main'
    }
}
```

---

### 7. How do you create multi-project builds in Gradle?

**Answer:**
Multi-project builds use `settings.gradle` to define projects.

**settings.gradle:**
```groovy
rootProject.name = 'parent-project'

include 'module1'
include 'module2'
include 'module3'

project(':module1').projectDir = file('modules/module1')
```

**Root build.gradle:**
```groovy
// Common configuration for all subprojects
subprojects {
    apply plugin: 'java'
    
    repositories {
        mavenCentral()
    }
    
    dependencies {
        testImplementation 'junit:junit:4.13.2'
    }
}

// Project-specific configuration
project(':module1') {
    dependencies {
        implementation project(':module2')
    }
}
```

**Module build.gradle:**
```groovy
dependencies {
    implementation project(':module2')
    implementation 'com.example:library:1.0.0'
}
```

**Building:**
```bash
# Build all projects
./gradlew build

# Build specific project
./gradlew :module1:build

# Build with dependencies
./gradlew :module1:build --include-build
```

---

### 8. How do you use Gradle Wrapper?

**Answer:**
Gradle Wrapper ensures consistent Gradle versions across environments.

**Generating Wrapper:**
```bash
gradle wrapper --gradle-version 7.5
```

**Wrapper Files:**
- `gradlew` / `gradlew.bat`: Wrapper scripts
- `gradle/wrapper/gradle-wrapper.jar`: Wrapper JAR
- `gradle/wrapper/gradle-wrapper.properties`: Wrapper configuration

**gradle-wrapper.properties:**
```properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-7.5-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

**Using Wrapper:**
```bash
# Unix/Mac
./gradlew build

# Windows
gradlew.bat build
```

**Benefits:**
- Consistent Gradle version
- No need to install Gradle
- Version controlled in project

---

### 9. How do you configure Gradle repositories?

**Answer:**
Repositories are configured in the `repositories` block.

**Repository Configuration:**
```groovy
repositories {
    // Maven Central
    mavenCentral()
    
    // Custom Maven repository
    maven {
        url 'https://repo.example.com/maven'
        credentials {
            username = 'user'
            password = 'pass'
        }
    }
    
    // Local Maven repository
    mavenLocal()
    
    // Ivy repository
    ivy {
        url 'https://repo.example.com/ivy'
    }
    
    // Flat directory
    flatDir {
        dirs 'libs'
    }
}
```

**Repository Order:**
- Gradle checks repositories in order
- First match wins
- Use `mavenCentral()` for public dependencies
- Use custom repositories for internal artifacts

---

### 10. How do you handle Gradle build variants and flavors?

**Answer:**
Build variants allow different builds from same source.

**Java Library Variants:**
```groovy
java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

// Different source sets
sourceSets {
    main {
        java.srcDirs = ['src/main/java']
        resources.srcDirs = ['src/main/resources']
    }
    test {
        java.srcDirs = ['src/test/java']
        resources.srcDirs = ['src/test/resources']
    }
}
```

**Android Build Variants:**
```groovy
android {
    flavorDimensions "version"
    
    productFlavors {
        dev {
            dimension "version"
            applicationIdSuffix ".dev"
            versionNameSuffix "-dev"
        }
        prod {
            dimension "version"
        }
    }
    
    buildTypes {
        debug {
            debuggable true
        }
        release {
            minifyEnabled true
        }
    }
}
```

---

### 11. How do you optimize Gradle builds?

**Answer:**
**Optimization Strategies:**

1. **Gradle Daemon:**
```properties
# gradle.properties
org.gradle.daemon=true
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configureondemand=true
```

2. **Build Cache:**
```groovy
// settings.gradle
buildCache {
    local {
        enabled = true
    }
    remote(HttpBuildCache) {
        url = 'https://cache.example.com/cache/'
    }
}
```

3. **Incremental Builds:**
- Gradle automatically detects changes
- Only rebuilds what's necessary

4. **Parallel Execution:**
```properties
org.gradle.parallel=true
org.gradle.workers.max=4
```

5. **Dependency Resolution:**
```groovy
configurations.all {
    resolutionStrategy {
        cacheDynamicVersionsFor 10, 'minutes'
        cacheChangingModulesFor 0, 'seconds'
    }
}
```

---

### 12. How do you troubleshoot Gradle build issues?

**Answer:**
**Common Issues and Solutions:**

1. **Dependency Resolution:**
```bash
# Check dependencies
./gradlew dependencies

# Check dependency insight
./gradlew dependencyInsight --dependency com.example:library

# Refresh dependencies
./gradlew --refresh-dependencies build
```

2. **Build Failures:**
```bash
# Clean build
./gradlew clean build

# Run with stacktrace
./gradlew build --stacktrace

# Run with debug
./gradlew build --debug

# Run with info
./gradlew build --info
```

3. **Cache Issues:**
```bash
# Clear cache
./gradlew clean --refresh-dependencies

# Stop daemon
./gradlew --stop
```

---

## 📝 **Best Practices**

1. **Use Gradle Wrapper**: Always commit wrapper files
2. **Use plugins block**: Prefer plugins DSL
3. **Dependency management**: Use version catalogs
4. **Build optimization**: Enable caching and parallel execution
5. **Task configuration**: Use lazy configuration
6. **Multi-project**: Organize with settings.gradle
7. **Properties**: Use gradle.properties for configuration
8. **Documentation**: Keep README updated
9. **Testing**: Run tests before deploying
10. **CI/CD**: Integrate with CI/CD pipelines

---

**Good luck with your Gradle interview preparation!**
