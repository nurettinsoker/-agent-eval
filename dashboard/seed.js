const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  // Create organization first
  const org = await prisma.organization.create({
    data: {
      name: "Default Org",
      slug: "default-org"
    }
  });
  console.log(`Created org: ${org.id} - ${org.name}`);

  const project = await prisma.project.create({
    data: {
      name: "Default Project",
      description: "Default project for evaluations",
      organizationId: org.id
    }
  });
  console.log(`Created project: ${project.id} - ${project.name}`);
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
