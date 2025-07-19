import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  ArrowRight,
  CheckCircle,
  Star,
  Users,
  Compass,
  Shield,
  Map,
  Sword,
  Menu,
  Trophy,
} from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export default function Homepage() {
  return (
    <div className="flex flex-col min-h-screen bg-black">
      {/* Header */}
      <header className="px-4 lg:px-6 h-16 flex items-center border-b border-green-800/30 bg-black/80">
        <Link className="flex items-center justify-center" href="#">
          <div className="h-8 w-8 bg-gradient-to-br from-green-700 to-green-900 rounded-lg flex items-center justify-center">
            <Compass className="h-5 w-5 text-green-100" />
          </div>
          <span className="ml-2 text-xl font-bold text-green-100">
            SideQuest
          </span>
        </Link>
        <nav className="ml-auto hidden md:flex gap-6">
          <Link
            className="text-sm font-medium hover:text-green-400 transition-colors text-green-200"
            href="#features"
          >
            Features
          </Link>
          <Link
            className="text-sm font-medium hover:text-green-400 transition-colors text-green-200"
            href="#quests"
          >
            Quests
          </Link>
          <Link
            className="text-sm font-medium hover:text-green-400 transition-colors text-green-200"
            href="#about"
          >
            About
          </Link>
          <Link
            className="text-sm font-medium hover:text-green-400 transition-colors text-green-200"
            href="#contact"
          >
            Contact
          </Link>
        </nav>
        <Button
          variant="ghost"
          size="icon"
          className="ml-4 md:hidden text-green-200 hover:text-green-400 hover:bg-green-900/20"
        >
          <Menu className="h-5 w-5" />
        </Button>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 bg-gradient-to-br from-black via-gray-950 to-black">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="space-y-2">
                <Badge
                  variant="secondary"
                  className="mb-4 bg-green-900/50 text-green-300 border-green-700/50"
                >
                  🗡️ New: Dark Adventures Await
                </Badge>
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none bg-gradient-to-r from-green-400 to-green-600 bg-clip-text text-transparent">
                  Embark on Your SideQuest
                </h1>
                <p className="mx-auto max-w-[700px] text-green-200 md:text-xl">
                  Discover hidden adventures in the shadows, complete dangerous
                  challenges, and unlock forbidden rewards. Join thousands of
                  rogues already exploring the underground.
                </p>
              </div>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  size="lg"
                  className="bg-gradient-to-r from-green-700 to-green-800 hover:from-green-600 hover:to-green-700 text-white border-green-600"
                >
                  Start Your Quest
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
                <Button
                  variant="outline"
                  size="lg"
                  className="border-green-600 text-green-300 hover:bg-green-900/30 bg-transparent"
                >
                  View Adventures
                </Button>
              </div>
              <div className="flex items-center gap-4 text-sm text-green-300 mt-8">
                <div className="flex items-center gap-1">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  <span>Free to start</span>
                </div>
                <div className="flex items-center gap-1">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  <span>No experience required</span>
                </div>
                <div className="flex items-center gap-1">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  <span>Dark rewards</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Social Proof */}
        <section className="w-full py-12 md:py-16 border-b border-green-800/30 bg-black/50">
          <div className="container px-4 md:px-6">
            <div className="text-center mb-8">
              <p className="text-sm text-green-300 mb-6">
                Trusted by over 50,000+ shadow adventurers worldwide
              </p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-8 items-center justify-center opacity-40">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="flex justify-center">
                  <Image
                    src={`/placeholder.svg?height=40&width=120&text=Guild${i}`}
                    alt={`Guild ${i} logo`}
                    width={120}
                    height={40}
                    className="h-8 w-auto filter brightness-75 hue-rotate-90"
                  />
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section
          id="features"
          className="w-full py-12 md:py-24 lg:py-32 bg-black"
        >
          <div className="container px-4 md:px-6">
            <div className="text-center mb-12">
              <Badge
                variant="secondary"
                className="mb-4 bg-green-900/50 text-green-300 border-green-700/50"
              >
                Features
              </Badge>
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-4 text-green-100">
                Everything you need for dark adventures
              </h2>
              <p className="mx-auto max-w-[700px] text-green-300 md:text-xl">
                Powerful tools and features designed to help you discover,
                track, and complete dangerous quests with fellow shadow
                adventurers.
              </p>
            </div>
            <div className="grid gap-6 lg:grid-cols-3 lg:gap-12">
              <Card className="border-green-800/50 shadow-lg hover:shadow-xl transition-shadow bg-gradient-to-br from-gray-950 to-black hover:border-green-700/70">
                <CardContent className="p-6">
                  <div className="h-12 w-12 bg-gradient-to-br from-green-600 to-green-800 rounded-lg flex items-center justify-center mb-4">
                    <Map className="h-6 w-6 text-green-100" />
                  </div>
                  <h3 className="text-xl font-bold mb-2 text-green-100">
                    Shadow Mapping
                  </h3>
                  <p className="text-green-300">
                    Discover hidden quests and underground adventures with our
                    stealth mapping system. Never miss a dark opportunity.
                  </p>
                </CardContent>
              </Card>
              <Card className="border-green-800/50 shadow-lg hover:shadow-xl transition-shadow bg-gradient-to-br from-gray-950 to-black hover:border-green-700/70">
                <CardContent className="p-6">
                  <div className="h-12 w-12 bg-gradient-to-br from-green-700 to-green-900 rounded-lg flex items-center justify-center mb-4">
                    <Shield className="h-6 w-6 text-green-100" />
                  </div>
                  <h3 className="text-xl font-bold mb-2 text-green-100">
                    Stealth Protection
                  </h3>
                  <p className="text-green-300">
                    Adventure safely in the shadows with our encrypted quest
                    system and anonymous community ratings.
                  </p>
                </CardContent>
              </Card>
              <Card className="border-green-800/50 shadow-lg hover:shadow-xl transition-shadow bg-gradient-to-br from-gray-950 to-black hover:border-green-700/70">
                <CardContent className="p-6">
                  <div className="h-12 w-12 bg-gradient-to-br from-green-600 to-green-800 rounded-lg flex items-center justify-center mb-4">
                    <Compass className="h-6 w-6 text-green-100" />
                  </div>
                  <h3 className="text-xl font-bold mb-2 text-green-100">
                    Dark Navigation
                  </h3>
                  <p className="text-green-300">
                    Advanced stealth GPS and night vision AR to guide you
                    through the most treacherous quests.
                  </p>
                </CardContent>
              </Card>
              <Card className="border-green-800/50 shadow-lg hover:shadow-xl transition-shadow bg-gradient-to-br from-gray-950 to-black hover:border-green-700/70">
                <CardContent className="p-6">
                  <div className="h-12 w-12 bg-gradient-to-br from-red-700 to-red-900 rounded-lg flex items-center justify-center mb-4">
                    <Sword className="h-6 w-6 text-red-100" />
                  </div>
                  <h3 className="text-xl font-bold mb-2 text-green-100">
                    Deadly Challenges
                  </h3>
                  <p className="text-green-300">
                    Take on forbidden challenges and prove your worth among the
                    most feared adventurers.
                  </p>
                </CardContent>
              </Card>
              <Card className="border-green-800/50 shadow-lg hover:shadow-xl transition-shadow bg-gradient-to-br from-gray-950 to-black hover:border-green-700/70">
                <CardContent className="p-6">
                  <div className="h-12 w-12 bg-gradient-to-br from-green-700 to-green-900 rounded-lg flex items-center justify-center mb-4">
                    <Users className="h-6 w-6 text-green-100" />
                  </div>
                  <h3 className="text-xl font-bold mb-2 text-green-100">
                    Shadow Guilds
                  </h3>
                  <p className="text-green-300">
                    Join forces with other rogues, form secret guilds, and
                    tackle underground group quests together.
                  </p>
                </CardContent>
              </Card>
              <Card className="border-green-800/50 shadow-lg hover:shadow-xl transition-shadow bg-gradient-to-br from-gray-950 to-black hover:border-green-700/70">
                <CardContent className="p-6">
                  <div className="h-12 w-12 bg-gradient-to-br from-yellow-700 to-green-800 rounded-lg flex items-center justify-center mb-4">
                    <Trophy className="h-6 w-6 text-yellow-200" />
                  </div>
                  <h3 className="text-xl font-bold mb-2 text-green-100">
                    Forbidden Rewards
                  </h3>
                  <p className="text-green-300">
                    Earn exclusive dark rewards, secret achievements, and
                    underground recognition for your deeds.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* Testimonials */}
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-br from-black to-gray-950/50">
          <div className="container px-4 md:px-6">
            <div className="text-center mb-12">
              <Badge
                variant="secondary"
                className="mb-4 bg-green-900/50 text-green-300 border-green-700/50"
              >
                Testimonials
              </Badge>
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-4 text-green-100">
                Stories from shadow adventurers
              </h2>
            </div>
            <div className="grid gap-6 lg:grid-cols-3">
              {[
                {
                  name: "Raven Nightwhisper",
                  role: "Shadow Master",
                  content:
                    "SideQuest has revealed a hidden world of adventures that exist in the darkness. Every quest is a dangerous story waiting to unfold.",
                  rating: 5,
                },
                {
                  name: "Vex Shadowbane",
                  role: "Guild Assassin",
                  content:
                    "The shadow guild system is incredible. We've completed over 50 underground quests and our bonds are forged in darkness.",
                  rating: 5,
                },
                {
                  name: "Nyx Grimheart",
                  role: "Lone Wolf",
                  content:
                    "From forbidden treasures to deadly challenges, SideQuest has made every night an adventure in the shadows.",
                  rating: 5,
                },
              ].map((testimonial, i) => (
                <Card
                  key={i}
                  className="border-green-800/50 shadow-lg bg-black/70 hover:bg-gray-950/90 transition-colors"
                >
                  <CardContent className="p-6">
                    <div className="flex mb-4">
                      {[...Array(testimonial.rating)].map((_, j) => (
                        <Star
                          key={j}
                          className="h-4 w-4 fill-green-500 text-green-500"
                        />
                      ))}
                    </div>
                    <p className="text-green-300 mb-4">
                      "{testimonial.content}"
                    </p>
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 bg-gradient-to-br from-green-600 to-green-800 rounded-full flex items-center justify-center text-green-100 font-semibold">
                        {testimonial.name
                          .split(" ")
                          .map((n) => n[0])
                          .join("")}
                      </div>
                      <div>
                        <p className="font-semibold text-green-100">
                          {testimonial.name}
                        </p>
                        <p className="text-sm text-green-400">
                          {testimonial.role}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-r from-green-800 to-green-900">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-green-100">
                  Your dark adventure awaits
                </h2>
                <p className="mx-auto max-w-[600px] text-green-200 md:text-xl">
                  Join thousands of shadow adventurers who have already
                  discovered the secrets of SideQuest.
                </p>
              </div>
              <div className="w-full max-w-sm space-y-2">
                <form className="flex gap-2">
                  <Input
                    type="email"
                    placeholder="Enter your email"
                    className="flex-1 bg-green-950/30 border-green-700/50 text-green-100 placeholder:text-green-400"
                  />
                  <Button
                    type="submit"
                    variant="secondary"
                    className="bg-green-100 text-green-900 hover:bg-green-200"
                  >
                    Begin Quest
                  </Button>
                </form>
                <p className="text-xs text-green-200">
                  Start your first shadow adventure today. No light required.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t border-green-800/30 bg-black/80">
        <p className="text-xs text-green-300">
          © 2024 SideQuest. All rights reserved.
        </p>
        <nav className="sm:ml-auto flex gap-4 sm:gap-6">
          <Link
            className="text-xs hover:underline underline-offset-4 text-green-300 hover:text-green-400"
            href="#"
          >
            Terms of Service
          </Link>
          <Link
            className="text-xs hover:underline underline-offset-4 text-green-300 hover:text-green-400"
            href="#"
          >
            Privacy Policy
          </Link>
          <Link
            className="text-xs hover:underline underline-offset-4 text-green-300 hover:text-green-400"
            href="#"
          >
            Shadow Guidelines
          </Link>
        </nav>
      </footer>
    </div>
  );
}
